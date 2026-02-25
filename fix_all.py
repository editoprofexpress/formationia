#!/usr/bin/env python3
"""
Three fixes applied to all 15 modules:
1. Title/heading colors: add --domain-color to :root, fix briefing-title + h3 inline colors
2. Remove progress bars: hide .briefing-progress via CSS (display:none)
3. Module 14 specific: add missing briefing-footer HTML (btn-prev + btn-next)
"""
import re, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Domain color map ──────────────────────────────────────────────────────────
DOMAIN_COLOR = {
    'module-01-demystifier-ia.html':         '#ff6b6b',
    'module-02-donnees-sous-influence.html':  '#ff6b6b',
    'module-05-art-de-la-consigne.html':      '#4ecdc4',
    'module-06-iteration-amelioration.html':  '#4ecdc4',
    'module-12-impact-environnemental.html':  '#95e1d3',
    'module-13-vie-privee-donnees.html':      '#95e1d3',
    'module15-le-tribunal-de-l-ia.html':      '#95e1d3',
}

# All 16 files that have a briefing-progress bar
ALL_MODULES = [
    'module-01-demystifier-ia.html',
    'module-02-donnees-sous-influence.html',
    'module-03-dans-la-tete-du-modele.html',
    'module-04-generer-sans-comprendre.html',
    'module-05-art-de-la-consigne.html',
    'module-06-iteration-amelioration.html',
    'module-07-co-creer-ia.html',
    'module-08-choisir-bon-usage.html',
    'module-09-hallucinations.html',
    'module-11-signal-falsifie.html',
    'module-12-impact-environnemental.html',
    'module-13-vie-privee-donnees.html',
    'module-14-ia-et-emploi.html',
    'module15-le-tribunal-de-l-ia.html',
    'module1.html',
]

# ── 1 + 2: Color fixes + progress bar removal ─────────────────────────────────
for fname in ALL_MODULES:
    content = open(fname, 'r', encoding='utf-8').read()
    changed = []

    # ── A) Add --domain-color to :root if needed ───────────────────────────
    if fname in DOMAIN_COLOR:
        hex_val = DOMAIN_COLOR[fname]
        if '--domain-color' not in content:
            content = re.sub(
                r'(:root\s*\{)',
                r'\1\n  --domain-color: ' + hex_val + ';',
                content, count=1
            )
            changed.append(f'added --domain-color:{hex_val} to :root')
        elif re.search(r'--domain-color\s*:\s*' + re.escape(hex_val), content) is None:
            # domain-color exists but with wrong value - update it
            content = re.sub(
                r'--domain-color\s*:\s*[^;]+;',
                f'--domain-color: {hex_val};',
                content, count=1
            )
            changed.append(f'updated --domain-color to {hex_val}')

        # ── B) Fix .briefing-title color ─────────────────────────────────
        def fix_briefing_title(m):
            block = m.group(0)
            fixed = re.sub(r'color\s*:\s*var\(--neon-green\)', 'color:var(--domain-color)', block)
            return fixed

        new_content, n = re.subn(
            r'\.briefing-title\s*\{[^}]+\}',
            fix_briefing_title,
            content
        )
        if new_content != content:
            content = new_content
            changed.append('briefing-title color → var(--domain-color)')

        # ── C) Fix h3 inline colors in lesson content ──────────────────
        # Replace color:var(--neon-green) in h3 tags that appear in lesson
        # content strings (inside template literals or direct HTML)
        new_content, n = re.subn(
            r'(<h3\s[^>]*style="[^"]*?)color\s*:\s*var\(--neon-green\)',
            r'\1color:var(--domain-color)',
            content
        )
        if new_content != content:
            content = new_content
            changed.append(f'h3 inline colors → var(--domain-color) ({n} occurrences)')

    # ── D) Hide progress bar ──────────────────────────────────────────────────
    # Add .briefing-progress { display:none; } in <style> if not already there
    if '<div class="briefing-progress">' in content or 'briefing-progress' in content:
        if '.briefing-progress{display:none' not in content and '.briefing-progress { display: none' not in content:
            # Insert before closing </style> of LAST <style> block
            content = re.sub(
                r'(</style>)',
                r'    .briefing-progress{display:none!important}\n\1',
                content, count=1
            )
            changed.append('progress bar hidden')

    open(fname, 'w', encoding='utf-8').write(content)
    status = ' | '.join(changed) if changed else 'no changes'
    print(f'{fname}: {status}')

# ── 3: Module 14 – add missing briefing-footer HTML ──────────────────────────
print('\n=== Module 14: adding missing briefing-footer ===')
content = open('module-14-ia-et-emploi.html', 'r', encoding='utf-8').read()

if 'id="btn-next"' not in content:
    # Insert footer before closing </div> of briefing-body/briefing-screen
    footer_html = '''
        <div class="briefing-footer">
            <button class="briefing-btn" id="btn-prev" onclick="prevLesson()" disabled>← Précédent</button>
            <button class="briefing-btn primary" id="btn-next" onclick="nextLesson()">Suivant →</button>
        </div>'''
    # Insert after the briefing-content div and before closing of briefing-screen
    content = content.replace(
        '        <div class="briefing-content" id="lesson-content"></div>\n    </div>\n\n</div>',
        '        <div class="briefing-content" id="lesson-content"></div>\n    </div>\n' + footer_html + '\n\n</div>'
    )
    # Also fix the null-unchecked line: btnNext.classList.add('primary')
    content = content.replace(
        '        if (btnNext) btnNext.textContent = \'Ouvrir le bureau ARIA →\';\n        btnNext.classList.add(\'primary\');',
        '        if (btnNext) { btnNext.textContent = \'Ouvrir le bureau ARIA →\'; btnNext.classList.add(\'primary\'); }'
    )
    open('module-14-ia-et-emploi.html', 'w', encoding='utf-8').write(content)
    print('  ✓ briefing-footer with btn-prev + btn-next added')
    print('  ✓ null-guard fixed on btnNext.classList.add')
else:
    print('  btn-next already present')

print('\nAll done!')
