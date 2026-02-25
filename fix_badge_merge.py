#!/usr/bin/env python3
"""
Merge module number into domain badge and remove standalone module-official-label:
  BEFORE: [Fondations IA]  +  Module n° 01 (white)
  AFTER:  [Fondations IA - Module n°01]  (no more white label)
"""
import re, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MODULES = [
    ('module-01-demystifier-ia.html',          '01'),
    ('module-02-donnees-sous-influence.html',   '02'),
    ('module-03-dans-la-tete-du-modele.html',   '03'),
    ('module-04-generer-sans-comprendre.html',  '04'),
    ('module-05-art-de-la-consigne.html',       '05'),
    ('module-06-iteration-amelioration.html',   '06'),
    ('module-07-co-creer-ia.html',              '07'),
    ('module-08-choisir-bon-usage.html',        '08'),
    ('module-09-hallucinations.html',           '09'),
    ('module-10-biais-algorithmiques.html',     '10'),
    ('module-11-signal-falsifie.html',          '11'),
    ('module-12-impact-environnemental.html',   '12'),
    ('module-13-vie-privee-donnees.html',       '13'),
    ('module-14-ia-et-emploi.html',             '14'),
]

for fname, num in MODULES:
    print(f'=== {fname} ===')
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update domain-badge-std: append "- Module n°NN" to its text content
    #    Pattern: <div class="domain-badge-std" style="...">DOMAIN NAME</div>
    def add_module_num(m):
        tag_open = m.group(1)  # everything up to >
        text     = m.group(2)  # inner text
        if f'Module n°{num}' in text:
            return m.group(0)  # already done
        return f'{tag_open}{text} - Module n°{num}</div>'

    new_content, n1 = re.subn(
        r'(<div class="domain-badge-std"[^>]*>)(.*?)</div>',
        add_module_num,
        content,
        flags=re.DOTALL
    )
    if n1 == 0:
        print(f'  WARNING: domain-badge-std not found')
    else:
        print(f'  ✓ domain-badge-std updated')

    # 2. Remove the standalone module-official-label div (any whitespace variants)
    new_content, n2 = re.subn(
        r'\n?\s*<div class="module-official-label">Module n°?\s*{}</div>'.format(num),
        '',
        new_content
    )
    if n2 == 0:
        # Try broader match (space or not between n° and num, leading zeros optional)
        new_content, n2 = re.subn(
            r'\n?\s*<div class="module-official-label">[^<]*</div>',
            '',
            new_content,
            count=1
        )
    if n2:
        print(f'  ✓ module-official-label removed')
    else:
        print(f'  WARNING: module-official-label not found/removed')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_content)

# module1.html: uses title-badge instead
print('=== module1.html ===')
with open('module1.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change "Module n° 01" to "Fondations IA - Module n°01"
old = '<div class="title-badge">Module n° 01</div>'
new = '<div class="title-badge">Fondations IA - Module n°01</div>'
if old in content:
    content = content.replace(old, new)
    print('  ✓ title-badge updated to "Fondations IA - Module n°01"')
else:
    print('  WARNING: title-badge text not found as expected')

with open('module1.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nAll done!')
