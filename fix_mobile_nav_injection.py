#!/usr/bin/env python3
"""Déplace le bloc <script>mobile nav</script> du mauvais </body> vers le dernier."""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

MOBILE_JS_BLOCK = """<script>
/* ──── NAVIGATION MOBILE ──────────────────────────────── */
(function(){
  var bar=document.createElement('div');
  bar.id='mobile-nav-bar';bar.className='mobile-nav-bar';
  bar.innerHTML='<button class="mobile-hamburger" onclick="toggleMobileNav()" aria-label="Menu">&#9776;</button>'
    +'<span class="mobile-nav-title">Navigation</span>'
    +'<div class="mobile-nav-arrows">'
    +'<button class="mobile-nav-arrow" id="mob-prev" onclick="prevLesson()">&#8592; Préc.</button>'
    +'<button class="mobile-nav-arrow" id="mob-next" onclick="nextLesson()">Suiv. &#8594;</button>'
    +'</div>';
  var ov=document.createElement('div');
  ov.id='briefing-nav-overlay';ov.className='briefing-nav-overlay';
  ov.setAttribute('onclick','closeMobileNav()');
  var body=document.querySelector('.briefing-body');
  if(body){body.parentNode.insertBefore(bar,body);body.parentNode.insertBefore(ov,body);}
})();
function toggleMobileNav(){
  var n=document.querySelector('.briefing-nav'),o=document.getElementById('briefing-nav-overlay');
  if(!n)return;
  n.classList.toggle('nav-open');o.classList.toggle('visible');
  document.body.style.overflow=n.classList.contains('nav-open')?'hidden':'';
}
function closeMobileNav(){
  var n=document.querySelector('.briefing-nav'),o=document.getElementById('briefing-nav-overlay');
  if(n)n.classList.remove('nav-open');
  if(o)o.classList.remove('visible');
  document.body.style.overflow='';
}
/* Fermeture auto du tiroir au clic sur un item nav (mobile) */
document.addEventListener('click',function(e){
  if(window.innerWidth>768)return;
  if(e.target.closest('.briefing-nav-item')&&document.querySelector('.briefing-nav.nav-open'))
    closeMobileNav();
});
</script>"""

ALL_MODULES = [
    'module1.html','module-01-demystifier-ia.html','module-02-donnees-sous-influence.html',
    'module-03-dans-la-tete-du-modele.html','module-04-generer-sans-comprendre.html',
    'module-05-art-de-la-consigne.html','module-06-iteration-amelioration.html',
    'module-07-co-creer-ia.html','module-08-choisir-bon-usage.html',
    'module-09-hallucinations.html','module-10-biais-algorithmiques.html',
    'module-11-signal-falsifie.html','module-12-impact-environnemental.html',
    'module-13-vie-privee-donnees.html','module-14-ia-et-emploi.html',
    'module15-le-tribunal-de-l-ia.html',
]

for fname in ALL_MODULES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path,'r',encoding='utf-8') as f: content = f.read()

    # 1. Supprimer TOUTES les occurrences du bloc mobile nav
    cleaned, n = re.subn(
        r'<script>\s*/\* ──── NAVIGATION MOBILE.*?</script>',
        '', content, flags=re.DOTALL
    )
    if n == 0:
        print(f'⚠  {fname}: bloc introuvable'); continue

    # 2. Injecter avant le DERNIER </body>
    pos = cleaned.rfind('</body>')
    if pos == -1:
        print(f'⚠  {fname}: pas de </body>'); continue

    result = cleaned[:pos] + MOBILE_JS_BLOCK + '\n' + cleaned[pos:]

    with open(path,'w',encoding='utf-8') as f: f.write(result)

    bodies  = result.count('</body>')
    js_ok   = result.rfind('toggleMobileNav') > result.rfind('</body>') - 200
    print(f'{"✅" if js_ok else "⚠"} {fname}  [retiré:{n} | </body>:{bodies} | pos_ok:{js_ok}]')

print('\n✅ Terminé.')
