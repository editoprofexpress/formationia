#!/usr/bin/env python3
"""
Comprehensive harmonization of all 15 modules.
Fixes:
1. Sidebar (briefing-nav) accent colors to match domain category
2. Back-link-sidebar HTML format (simple text → proper spans)
3. Certificate nav item (add where missing)
4. Separator before game/mission items
5. Back-link text "Retour modules" → "Tous les modules"
"""
import re, os, sys

BASE = '/home/user/formationia'

# ── Category colors ────────────────────────────────────────────────────────────
COLORS = {
    'red':    {'hex': '#ff6b6b', 'rgb': '255,107,107'},   # Fondations IA
    'cyan':   {'hex': '#4ecdc4', 'rgb': '78,205,196'},    # Interaction Raisonnée
    'yellow': {'hex': '#ffe66d', 'rgb': '255,230,109'},   # Limites & Esprit Critique
    'mint':   {'hex': '#95e1d3', 'rgb': '149,225,211'},   # Enjeux Citoyens
}

# Module → color mapping
MODULE_COLOR = {
    'module-01-demystifier-ia.html':       'red',
    'module-02-donnees-sous-influence.html':'red',
    'module-03-dans-la-tete-du-modele.html':'red',
    'module-04-generer-sans-comprendre.html':'red',
    'module-05-art-de-la-consigne.html':   'cyan',
    'module-06-iteration-amelioration.html':'cyan',
    'module-07-co-creer-ia.html':          'cyan',
    'module-08-choisir-bon-usage.html':    'cyan',
    'module-09-hallucinations.html':       'yellow',
    'module-10-biais-algorithmiques.html': 'yellow',
    'module-11-signal-falsifie.html':      'yellow',
    'module-12-impact-environnemental.html':'mint',
    'module-13-vie-privee-donnees.html':   'mint',
    'module-14-ia-et-emploi.html':         'mint',
    'module15-le-tribunal-de-l-ia.html':   'mint',
}

def domain_css_override(color_name):
    c = COLORS[color_name]
    hex_ = c['hex']
    rgb  = c['rgb']
    return f"""
    /* ==================== COULEURS DOMAINE SIDEBAR ==================== */
    .briefing-nav {{ border-right-color: rgba({rgb},0.2) !important; }}
    .briefing-nav::-webkit-scrollbar-thumb {{ background: rgba({rgb},0.3) !important; border-radius: 2px; }}
    .back-link-sidebar {{
      background: rgba({rgb},0.05) !important;
      border-color: rgba({rgb},0.3) !important;
      color: {hex_} !important;
    }}
    .back-link-sidebar:hover {{
      background: rgba({rgb},0.15) !important;
      border-color: {hex_} !important;
    }}
    .briefing-nav-item:hover {{ background: rgba({rgb},0.05) !important; }}
    .briefing-nav-item.active {{
      border-left-color: {hex_} !important;
      background: rgba({rgb},0.1) !important;
      color: {hex_} !important;
    }}
    .nav-number {{ background: rgba({rgb},0.2) !important; }}
    .briefing-nav-item.active .nav-number {{ background: rgba({rgb},0.4) !important; }}
"""

# Standard structured back-link HTML
BACK_LINK_STANDARD = '''<a href="modules.html" class="back-link-sidebar" title="Retour à la liste des modules">
          <span class="back-arrow">←</span><span>Tous les modules</span>
        </a>'''

# Standard certificate nav item HTML
CERT_NAV_ITEM = '''          <div class="briefing-nav-item" id="certificate-nav-item" onclick="showCertificateInFolder()" style="opacity:0.5;cursor:not-allowed;background:rgba(100,100,100,0.2)">
            <span class="nav-icon">🔒</span>
            <span class="nav-number" style="background:rgba(100,100,100,0.3);color:#888">--</span>
            Attestation de réussite
          </div>'''

def read(fname):
    with open(os.path.join(BASE, fname), encoding='utf-8') as f:
        return f.read()

def write(fname, content):
    with open(os.path.join(BASE, fname), 'w', encoding='utf-8') as f:
        f.write(content)

def apply_css_override(html, color_name):
    """Inject domain sidebar CSS override into the HARMONISATION TITRE block."""
    override = domain_css_override(color_name)
    # Skip if already injected
    if 'COULEURS DOMAINE SIDEBAR' in html:
        # Replace existing block
        html = re.sub(
            r'\n    /\* ={10,} COULEURS DOMAINE SIDEBAR ={10,} \*/.*?(?=\n    /\* =|</style>)',
            '',
            html, flags=re.DOTALL
        )
    # Inject before closing </style>
    html = html.replace('</style>', override + '\n</style>', 1)
    return html

def fix_back_link(html, filename):
    """Standardize the back-link-sidebar HTML format."""
    # Patterns to replace:
    # 1. Simple: <a href="modules.html" class="back-link-sidebar">← Tous les modules</a>
    # 2. Partial spans: <a ... class="back-link-sidebar">← Tous les modules</a>
    # 3. Wrong text: "← Retour modules" or "← Retour aux modules"

    # Replace various back-link patterns with standard format
    patterns = [
        # Simple text versions
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>\s*←\s*Tous les modules\s*</a>',
         BACK_LINK_STANDARD),
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>\s*←\s*Retour modules\s*</a>',
         BACK_LINK_STANDARD),
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>←\s*Retour modules</a>',
         BACK_LINK_STANDARD),
        # Version with back-arrow span but wrong text
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>\s*<span[^>]*>←</span>\s*Retour modules\s*</a>',
         BACK_LINK_STANDARD),
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>\s*<span[^>]*class="back-arrow"[^>]*>←</span>\s*Retour modules\s*</a>',
         BACK_LINK_STANDARD),
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>\s*<span[^>]*class="back-arrow"[^>]*>←</span>\s*<span>Tous les modules</span>\s*</a>',
         BACK_LINK_STANDARD),
        # Version with just span without class
        (r'<a\s+href="modules\.html"\s+class="back-link-sidebar"[^>]*>\s*<span>←</span><span>Tous les modules</span>\s*</a>',
         BACK_LINK_STANDARD),
    ]
    for pattern, replacement in patterns:
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    return html

def has_cert_nav_item(html):
    return 'id="certificate-nav-item"' in html

def add_cert_nav_item(html, filename):
    """Add certificate nav item to the briefing-nav sidebar where missing."""

    # For module-03: fix existing cert-nav-item (display:none → visible locked)
    if 'module-03' in filename:
        # Replace the cert-nav-item (display:none) with visible locked version
        html = re.sub(
            r'<div class="briefing-nav-item"\s+id="cert-nav-item"\s+onclick="showCertInBriefing\(\)"\s+style="display:none">.*?</div>',
            '''<div class="briefing-nav-item" id="certificate-nav-item" onclick="showCertificateInFolder()" style="opacity:0.5;cursor:not-allowed;background:rgba(100,100,100,0.2)">
            <span class="nav-icon">🔒</span>
            <span class="nav-number" style="background:rgba(100,100,100,0.3);color:#888">--</span>
            Attestation de réussite
          </div>''',
            html, flags=re.DOTALL
        )
        # Update unlockCertificate to use new id and opacity approach
        html = html.replace(
            '''function unlockCertificate() {
      certificateUnlocked = true;
      const cNav = document.getElementById('cert-nav-item');
      if (cNav) {
        cNav.style.display = '';
        cNav.querySelector('.nav-icon').textContent = '🎓';
      }
      showCertInBriefing();
    }''',
            '''function unlockCertificate() {
      certificateUnlocked = true;
      const navItem = document.getElementById('certificate-nav-item');
      if (navItem) {
        navItem.style.opacity = '1';
        navItem.style.cursor = 'pointer';
        navItem.style.background = '';
        const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
        const num = navItem.querySelector('.nav-number');
        if (num) { num.style.background = 'rgba(0,255,136,0.2)'; num.style.color = 'var(--neon-green)'; num.textContent = '✓'; }
      }
      showCertificateInFolder();
    }
    function showCertificateInFolder() { showCertInBriefing(); }'''
        )
        # Also update showCertInBriefing to reference certificate-nav-item
        html = html.replace("document.getElementById('cert-nav-item')", "document.getElementById('certificate-nav-item')")
        return html

    # For module-11: add cert nav item after existing mission item + update unlockCertificate
    if 'module-11' in filename:
        # The module-11 nav ends with a separator section containing "Salle d'analyse"
        # Add cert nav item within that section
        # Find the closing pattern of the separator div containing the mission item
        # Pattern: the nav ends with the briefing-nav closing tag
        # Insert cert nav item before </nav>
        html = re.sub(
            r'(</nav>)(\s*\n\s*<div class="briefing-content")',
            '''        <div class="briefing-nav-item" id="certificate-nav-item" onclick="showCertificateInFolder()" style="opacity:0.5;cursor:not-allowed;background:rgba(100,100,100,0.2)">
            <span class="nav-icon">🔒</span>
            <span class="nav-number" style="background:rgba(100,100,100,0.3);color:#888">--</span>
            Attestation de réussite
          </div>
      \\1\\2''',
            html, count=1, flags=re.DOTALL
        )
        # Update unlockCertificate to also update nav item
        old_unlock = 'function unlockCertificate(){\n  certificateUnlocked = true;\n}'
        new_unlock = '''function unlockCertificate(){
  certificateUnlocked = true;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(0,255,136,0.2)'; num.style.color = 'var(--neon-green)'; num.textContent = '✓'; }
  }
  toast('🎓 Attestation débloquée !', 3500);
}
function showCertificateInFolder() { showCertificate(); }'''
        html = html.replace(old_unlock, new_unlock)
        return html

    # For modules 04, 05, 07, 08, 10, 14: add cert nav item before </nav>
    # Also add separator + cert nav if no separator exists for those without any separator section

    # Module-specific JS to add (unlockCertificate + showCertificateInFolder)
    cert_js = {}

    cert_js['module-04'] = '''
/* ==================== ATTESTATION SIDEBAR ==================== */
let certFinalPct04 = 0;
function unlockCertificate(pct) {
  certFinalPct04 = pct || certFinalPct04;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(255,107,107,0.2)'; num.style.color = '#ff6b6b'; num.textContent = '✓'; }
  }
}
function showCertificateInFolder() {
  // Show quiz/cert screen for attestation
  const qs = document.getElementById('quiz-screen');
  if (qs) { qs.style.display = 'flex'; }
  const bs = document.getElementById('briefing-screen');
  if (bs) { bs.classList.remove('active'); }
}'''

    cert_js['module-05'] = '''
/* ==================== ATTESTATION SIDEBAR ==================== */
let certFinalPct05 = 0;
function unlockCertificate(pct) {
  certFinalPct05 = pct || certFinalPct05;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(78,205,196,0.2)'; num.style.color = '#4ecdc4'; num.textContent = '✓'; }
  }
}
function showCertificateInFolder() {
  // Show the quiz screen which has the attestation section
  const qs = document.getElementById('quiz-screen');
  if (qs) { qs.style.display = 'flex'; }
  const bs = document.getElementById('briefing-screen');
  if (bs) { bs.classList.remove('active'); }
}'''

    cert_js['module-07'] = '''
/* ==================== ATTESTATION SIDEBAR ==================== */
let certUnlocked07 = false;
function unlockCertificate(score) {
  certUnlocked07 = true;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(78,205,196,0.2)'; num.style.color = '#4ecdc4'; num.textContent = '✓'; }
  }
}
function showCertificateInFolder() {
  if (!certUnlocked07) return;
  const qs = document.getElementById('quiz-screen');
  if (qs) { qs.style.display = 'flex'; }
  const bs = document.getElementById('briefing-screen');
  if (bs) { bs.classList.remove('active'); }
  startCertification(finalScore);
}'''

    cert_js['module-08'] = '''
/* ==================== ATTESTATION SIDEBAR ==================== */
function unlockCertificate() {
  certUnlocked = true;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(78,205,196,0.2)'; num.style.color = '#4ecdc4'; num.textContent = '✓'; }
  }
}
function showCertificateInFolder() { showCertificate(); }'''

    cert_js['module-10'] = '''
/* ==================== ATTESTATION SIDEBAR ==================== */
let certUnlocked10 = false;
function unlockCertificate(pct) {
  certUnlocked10 = true;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(255,230,109,0.2)'; num.style.color = '#ffe66d'; num.textContent = '✓'; }
  }
}
function showCertificateInFolder() { if (certUnlocked10) showCertificate(quizScore); }'''

    cert_js['module-14'] = '''
/* ==================== ATTESTATION SIDEBAR ==================== */
let certUnlocked14 = false;
function unlockCertificate(pct) {
  certUnlocked14 = true;
  const navItem = document.getElementById('certificate-nav-item');
  if (navItem) {
    navItem.style.opacity = '1'; navItem.style.cursor = 'pointer'; navItem.style.background = '';
    const icon = navItem.querySelector('.nav-icon'); if (icon) icon.textContent = '🎓';
    const num = navItem.querySelector('.nav-number');
    if (num) { num.style.background = 'rgba(149,225,211,0.2)'; num.style.color = '#95e1d3'; num.textContent = '✓'; }
  }
}
function showCertificateInFolder() {
  if (!certUnlocked14) return;
  const bs = document.getElementById('briefing-screen');
  if (bs) bs.classList.add('active');
  // Navigate to quiz lesson which has the attestation
  showLesson(7);
}'''

    # Find which module this is
    mod_key = None
    for k in cert_js:
        if k in filename:
            mod_key = k
            break

    if mod_key is None:
        # Fallback: just add nav item before </nav>
        pass

    # Add the cert nav item before </nav> (first occurrence in briefing-nav)
    # Add separator + cert nav item
    # For module-10 which has dynamic nav (<div id="nav-items"></div>), insert differently
    if 'module-10' in filename:
        old = '<div id="nav-items"></div>\n</nav>'
        new = '''<div id="nav-items"></div>
      <div style="border-top:1px solid rgba(255,230,109,0.2);margin-top:15px;padding-top:15px">
        <div class="briefing-nav-item" id="certificate-nav-item" onclick="showCertificateInFolder()" style="opacity:0.5;cursor:not-allowed;background:rgba(100,100,100,0.2)">
          <span class="nav-icon">🔒</span>
          <span class="nav-number" style="background:rgba(100,100,100,0.3);color:#888">--</span>
          Attestation de réussite
        </div>
      </div>
</nav>'''
        html = html.replace(old, new, 1)
    else:
        # For other modules: inject cert nav item + separator before first </nav>
        # Find the first </nav> after briefing-nav opening
        match = re.search(r'<nav class="briefing-nav"[^>]*>.*?</nav>', html, re.DOTALL)
        if match:
            nav_html = match.group(0)
            nav_end = nav_html.rfind('</nav>')

            # Check if there's already a separator section at the bottom
            has_separator = 'border-top' in nav_html[-500:] or 'border-top' in nav_html[-1000:]

            if has_separator:
                # Just add cert nav item before </nav>
                insertion = '\n        ' + CERT_NAV_ITEM.strip() + '\n      '
            else:
                # Add separator + cert nav item
                insertion = '''
        <div style="border-top:1px solid rgba(0,212,255,0.2);margin-top:15px;padding-top:15px">
''' + '          ' + CERT_NAV_ITEM.strip() + '''
        </div>
      '''

            new_nav_html = nav_html[:nav_end] + insertion + '</nav>'
            html = html[:match.start()] + new_nav_html + html[match.end():]

    # Add the JS functions before </script> (last script tag)
    if mod_key and mod_key in cert_js:
        js_to_add = cert_js[mod_key]
        # Insert before last </script>
        last_script = html.rfind('</script>')
        if last_script >= 0:
            html = html[:last_script] + js_to_add + '\n' + html[last_script:]

    return html

def hook_unlock_certificate(html, filename):
    """After quiz success (pct >= 70), also call unlockCertificate()."""

    if 'module-04' in filename:
        # In submitQuiz, after success condition, add unlockCertificate(pct)
        # The success part does: quizAnswers, score calculation, then shows cert button
        # We need to call unlockCertificate(pct) after pct calculation
        # Find the success branch in submitQuiz
        old = '''    function submitQuiz() {
      let score = 0;
      quizQuestions.forEach((q, i) => { if (quizAnswers[i] === q.correct) score++; });
      const pct = Math.round(score / quizQuestions.length * 100);'''
        new = '''    function submitQuiz() {
      let score = 0;
      quizQuestions.forEach((q, i) => { if (quizAnswers[i] === q.correct) score++; });
      const pct = Math.round(score / quizQuestions.length * 100);
      if (pct >= 70) unlockCertificate(pct);'''
        html = html.replace(old, new, 1)

    elif 'module-05' in filename:
        # In submitQuiz5, success handling - add unlockCertificate call
        # Find where score and pct are calculated and success is determined
        old = "    const pass = pct >= 70;"
        new = "    const pass = pct >= 70;\n    if (pass) unlockCertificate(pct);"
        if old in html:
            html = html.replace(old, new, 1)

    elif 'module-07' in filename:
        # In submitQuiz, passed = pct >= 70
        # startCertification is called on button click
        # Add unlockCertificate call when passed
        old = "    const passed = pct >= 70;"
        new = "    const passed = pct >= 70;\n    if (passed) unlockCertificate(score);"
        if old in html:
            # Only replace the first occurrence (in submitQuiz)
            html = html.replace(old, new, 1)

    elif 'module-08' in filename:
        # certUnlocked = true is already set in submitQuiz
        # Add unlockCertificate() call after that
        old = "    if (passed) certUnlocked = true;"
        new = "    if (passed) { certUnlocked = true; unlockCertificate(); }"
        if old in html:
            html = html.replace(old, new, 1)

    elif 'module-10' in filename:
        # In submitQuiz, find the success branch
        # showCertificate(pct) is called on button click
        # Add unlockCertificate call when passed
        old = "if(passed){"
        new = "if(passed){ unlockCertificate(pct);"
        # Only the first occurrence (submitQuiz success)
        if old in html:
            html = html.replace(old, new, 1)

    elif 'module-14' in filename:
        # In submitAllQuiz, success handling
        # finalQuizScore >= 70 is checked
        old = "    const passed = finalQuizScore >= 70;"
        new = "    const passed = finalQuizScore >= 70;\n    if (passed) unlockCertificate(finalQuizScore);"
        if old in html:
            html = html.replace(old, new, 1)

    return html

def process_module(filename):
    print(f"\nProcessing {filename}...")
    html = read(filename)
    changed = False

    color_name = MODULE_COLOR.get(filename)
    if not color_name:
        print(f"  WARNING: No color mapping for {filename}")
        return

    # 1. Apply CSS color override
    # Skip modules that are already correct AND have correct back-link color:
    # Module 07 and 08 are already correct (cyan)
    # But even they may need the CSS block for consistency
    html_new = apply_css_override(html, color_name)
    if html_new != html:
        print(f"  + CSS color override added for {color_name}")
        html = html_new
        changed = True

    # 2. Fix back-link HTML format
    html_new = fix_back_link(html, filename)
    if html_new != html:
        print(f"  + Back-link HTML fixed")
        html = html_new
        changed = True

    # 3. Add certificate nav item if missing (+ separator + JS functions)
    if not has_cert_nav_item(html):
        html_new = add_cert_nav_item(html, filename)
        if html_new != html:
            print(f"  + Certificate nav item added")
            html = html_new
            changed = True

            # 4. Hook unlockCertificate into quiz success
            html_new2 = hook_unlock_certificate(html, filename)
            if html_new2 != html:
                print(f"  + unlockCertificate() hooked into quiz success")
                html = html_new2

    if changed:
        write(filename, html)
        print(f"  ✓ Saved {filename}")
    else:
        print(f"  → No changes needed")

# Process all modules
for fname in sorted(MODULE_COLOR.keys()):
    process_module(fname)

print("\nDone! All modules processed.")
