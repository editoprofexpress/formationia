#!/usr/bin/env python3
"""
Correctif responsive pour les 15 modules :
  1. Ajoute une barre de navigation mobile (hamburger + flèches prev/next)
     avec le sidebar en tiroir (drawer) sur mobile
  2. Supprime max-width:900px + margin:0 auto de .briefing-content
     pour que le contenu utilise tout l'espace disponible
"""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ── CSS injecté dans le bloc de standardisation ──────────────────────────────
MOBILE_CSS = """
    /* ──── NAVIGATION MOBILE ──────────────────────── */
    .mobile-nav-bar{display:none;align-items:center;gap:10px;padding:10px 16px;background:rgba(5,10,25,0.97);border-bottom:1px solid rgba(0,229,204,0.2);position:sticky;top:0;z-index:50;flex-shrink:0}
    .mobile-hamburger{background:transparent;border:1px solid var(--domain-color,#00e5cc);color:var(--domain-color,#00e5cc);font-size:1.2em;width:36px;height:36px;cursor:pointer;border-radius:4px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
    .mobile-nav-title{flex:1;font-size:0.78em;color:#8899aa;font-family:'Space Mono',monospace;letter-spacing:1px;text-transform:uppercase;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:0 6px}
    .mobile-nav-arrows{display:flex;gap:6px;flex-shrink:0}
    .mobile-nav-arrow{background:rgba(0,229,204,0.08);border:1px solid rgba(0,229,204,0.25);color:#cdd6f4;padding:7px 13px;cursor:pointer;border-radius:4px;font-size:0.85em;font-family:inherit;transition:background .2s}
    .mobile-nav-arrow:hover{background:rgba(0,229,204,0.2)}
    .mobile-nav-arrow:disabled{opacity:0.25;cursor:not-allowed}
    .briefing-nav-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.65);z-index:998;cursor:pointer}
    @media(max-width:768px){
      .mobile-nav-bar{display:flex}
      .briefing-nav.nav-open{display:flex!important;flex-direction:column;position:fixed;top:0;left:0;width:min(290px,85vw);height:100vh;z-index:999;overflow-y:auto;box-shadow:4px 0 24px rgba(0,0,0,0.7)}
      .briefing-nav-overlay.visible{display:block}
      .briefing-content{max-width:100%!important;margin:0!important;padding:16px 16px 60px!important}
    }"""

# ── JS injecté juste avant </body> ────────────────────────────────────────────
MOBILE_JS = """<script>
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
</script>
</body>"""

ALL_MODULES = [
    'module1.html',
    'module-01-demystifier-ia.html',
    'module-02-donnees-sous-influence.html',
    'module-03-dans-la-tete-du-modele.html',
    'module-04-generer-sans-comprendre.html',
    'module-05-art-de-la-consigne.html',
    'module-06-iteration-amelioration.html',
    'module-07-co-creer-ia.html',
    'module-08-choisir-bon-usage.html',
    'module-09-hallucinations.html',
    'module-10-biais-algorithmiques.html',
    'module-11-signal-falsifie.html',
    'module-12-impact-environnemental.html',
    'module-13-vie-privee-donnees.html',
    'module-14-ia-et-emploi.html',
    'module15-le-tribunal-de-l-ia.html',
]

FOOTER_MARKER = '.briefing-footer{display:none!important}'

def remove_content_constraints(content):
    """Supprime max-width:900px et margin:0 auto de .briefing-content (hors @media)."""
    # On retire max-width: 900px et margin: 0 auto dans TOUTES les règles
    # .briefing-content qui ne sont PAS dans un bloc @media
    # Stratégie : retrait global des lignes/fragments spécifiques
    # (ces valeurs n'apparaissent que dans .briefing-content dans ces fichiers)

    # Format compact : max-width:900px;   ou   max-width: 900px;
    content = re.sub(r'max-width\s*:\s*900px\s*;?\s*', '', content)

    # margin: 0 auto  SEULEMENT dans .briefing-content (pattern multiligne ou compact)
    # Pour éviter de supprimer d'autres margin:0 auto, on cherche le contexte
    # Compact : .briefing-content{...margin:0 auto...}
    content = re.sub(
        r'(\.briefing-content\b[^{]*\{[^}]*)margin\s*:\s*0\s+auto\s*;?\s*',
        r'\1',
        content,
        count=2  # max 2 occurrences (cas reset dans @media possible)
    )
    return content

for fname in ALL_MODULES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  Introuvable : {fname}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # ── 1. CSS mobile nav ────────────────────────────────────────────────────
    if 'mobile-nav-bar' in content:
        issues.append('css_already')
    elif FOOTER_MARKER in content:
        content = content.replace(FOOTER_MARKER, FOOTER_MARKER + MOBILE_CSS, 1)
        issues.append('css_ok')
    else:
        # Fallback : injecter avant </style> (première occurrence)
        content = content.replace('</style>', MOBILE_CSS + '\n</style>', 1)
        issues.append('css_fallback')

    # ── 2. Supprimer max-width:900px + margin:0 auto de .briefing-content ────
    before = content
    content = remove_content_constraints(content)
    issues.append('width_ok' if content != before else 'width_noop')

    # ── 3. JS mobile nav ─────────────────────────────────────────────────────
    if 'initMobileNav' in content or 'toggleMobileNav' in content:
        issues.append('js_already')
    elif '</body>' in content:
        content = content.replace('</body>', MOBILE_JS, 1)
        issues.append('js_ok')
    else:
        issues.append('js_missing_body')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    status = ' | '.join(issues)
    print(f'{"✅" if "already" not in status or "ok" in status else "⚠"} {fname}  [{status}]')

print('\n✅ Terminé.')
