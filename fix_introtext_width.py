#!/usr/bin/env python3
"""
Fix intro-text width on all modules:
- Add max-width CSS override in STANDARDISATION block
- Fix module-13 h1 title
"""
import re
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MODULES = [
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
    'module1.html',
]

# CSS rule to add — normalizes all intro-text to centered narrow column, no box
INTRO_CSS_LINE = '    #title-screen .intro-text { max-width: 680px !important; margin: 0 auto 32px !important; text-align: center !important; line-height: 1.85 !important; color: #aabbcc !important; font-size: 1.05em !important; padding: 0 20px !important; background: none !important; border: none !important; border-radius: 0 !important; box-shadow: none !important; }'

SIDEBAR_MARKER = '/* === STANDARDISATION FORMAT SIDEBAR === */'
CLOSING_LINE = '.briefing-title { font-size: 1.3em !important; }'

for fname in MODULES:
    print(f'=== {fname} ===')
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    sidebar_pos = content.find(SIDEBAR_MARKER)
    if sidebar_pos == -1:
        print(f'  WARNING: No STANDARDISATION block found')
        continue

    closing_pos = content.find(CLOSING_LINE, sidebar_pos)
    if closing_pos == -1:
        print(f'  WARNING: Closing line not found after STANDARDISATION block')
        continue

    # Check if already has the rule
    block = content[sidebar_pos:closing_pos + len(CLOSING_LINE)]
    if '#title-screen .intro-text' in block:
        print(f'  Already has intro-text rule — skipping')
        continue

    # Insert after the closing line
    insert_at = closing_pos + len(CLOSING_LINE)
    content = content[:insert_at] + '\n' + INTRO_CSS_LINE + content[insert_at:]
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✓ intro-text width rule added')

# Fix module-13 h1
print('\n=== Fix module-13 h1 ===')
fname13 = 'module-13-vie-privee-donnees.html'
with open(fname13, 'r', encoding='utf-8') as f:
    c = f.read()

old = '<h1 class="main-title">Données personnelles en danger</h1>'
new = '<h1 class="main-title">Vie privée & données</h1>'
if old in c:
    c = c.replace(old, new)
    with open(fname13, 'w', encoding='utf-8') as f:
        f.write(c)
    print('  ✓ h1 fixed → "Vie privée & données"')
else:
    print('  WARNING: Could not find expected h1 in module-13')

print('\nAll done!')
