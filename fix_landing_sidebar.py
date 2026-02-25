#!/usr/bin/env python3
"""
Fix landing pages + standardize sidebars across all 14 modules.

Landing page changes:
  1. Module name as BIG gradient title (correct domain colors)
  2. Mission/universe name as small subtitle (.mission-label)
  3. module-official-label simplified to "Module n° NN"
  4. .start-btn color matches domain

Sidebar changes:
  5. Standardize layout CSS to match module-02 reference
     (padding, font-size, nav-number styling, nav width, briefing-title size)
"""

import re, os

BASE = '/home/user/formationia'

# Module data: file, module name, mission label, domain color
MODULES = [
    ('module-01-demystifier-ia.html',    "Démystifier l'IA",              "DOSSIER ZÉRO  ·  VERIT-IA",         '01', '#ff6b6b', 'rgba(255,107,107)', "DOSSIER ZÉRO"),
    ('module-02-donnees-sous-influence.html', "Données sous influence",   "LABORATOIRES SYNAPTIK",              '02', '#ff6b6b', 'rgba(255,107,107)', "DONNÉES SOUS INFLUENCE"),
    ('module-03-dans-la-tete-du-modele.html', "Dans la tête du modèle",   "NEURONAUTE",                         '03', '#ff6b6b', 'rgba(255,107,107)', "NEURONAUTE"),
    ('module-04-generer-sans-comprendre.html',"Générer sans comprendre",  "SYNTHÈSE",                           '04', '#ff6b6b', 'rgba(255,107,107)', "SYNTHÈSE"),
    ('module-05-art-de-la-consigne.html', "L'art de la consigne",         "ARIA-7 LAB",                         '05', '#4ecdc4', 'rgba(78,205,196)',   "L'Art de la Consigne"),
    ('module-06-iteration-amelioration.html', "Itération et amélioration","STUDIO ITERATEK",                    '06', '#4ecdc4', 'rgba(78,205,196)',   "ITÉRATION & AMÉLIORATION"),
    ('module-07-co-creer-ia.html',        "Co-créer avec l'IA",           "SYNAPSE STUDIO",                     '07', '#4ecdc4', 'rgba(78,205,196)',   "SYNAPSE STUDIO"),
    ('module-08-choisir-bon-usage.html',  "Choisir le bon usage",         "NEXUS DÉCISION",                     '08', '#4ecdc4', 'rgba(78,205,196)',   "NEXUS DÉCISION"),
    ('module-09-hallucinations.html',     "L'erreur qui sonne juste",     "RÉDACTION VERITAS NEWS",             '09', '#ffe66d', 'rgba(255,230,109)',  "L'ERREUR QUI SONNE JUSTE"),
    ('module-10-biais-algorithmiques.html',"Biais invisibles",            "AGENCE EQUITYWATCH",                 '10', '#ffe66d', 'rgba(255,230,109)',  "BIAIS INVISIBLES"),
    ('module-11-signal-falsifie.html',    "Signal Falsifié",              "UNITÉ VERITAS",                      '11', '#ffe66d', 'rgba(255,230,109)',  "Signal Falsifié"),
    ('module-12-impact-environnemental.html', "Impact environnemental de l'IA", "INFILTRATION VERTE",          '12', '#95e1d3', 'rgba(149,225,211)',  "Green Infiltration"),
    ('module-13-vie-privee-donnees.html', "Données personnelles en danger","AGENCE SHIELD DATA",               '13', '#95e1d3', 'rgba(149,225,211)',  "Data Shadow"),
    ('module-14-ia-et-emploi.html',       "IA et Emploi",                 "AGENCE ARIA",                       '14', '#95e1d3', 'rgba(149,225,211)',  "SHIFT"),
]

GRADIENTS = {
    '#ff6b6b': ('linear-gradient(90deg,#ff6b6b,#ff8c00,#ff0080)', 'rgba(255,107,107,.5)'),
    '#4ecdc4': ('linear-gradient(90deg,#4ecdc4,#00d4ff,#a855f7)', 'rgba(78,205,196,.5)'),
    '#ffe66d': ('linear-gradient(90deg,#ffe66d,#ff8c00,#ff0080)', 'rgba(255,230,109,.5)'),
    '#95e1d3': ('linear-gradient(90deg,#95e1d3,#7ecdc4,#b5f5ec)', 'rgba(149,225,211,.5)'),
}

def read(fn):
    with open(os.path.join(BASE, fn), 'r', encoding='utf-8') as f:
        return f.read()

def write(fn, content):
    with open(os.path.join(BASE, fn), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {fn}")


def fix_module(filename, mod_name, mission_label, num, color, rgba_base, old_title):
    content = read(filename)
    gradient, shadow = GRADIENTS[color]
    rgba = rgba_base.rstrip(')')

    # ----------------------------------------------------------
    # 1. CSS: Update #title-screen .main-title in HARMONISATION block
    # ----------------------------------------------------------
    old_main_css = (
        '    #title-screen .main-title {\n'
        '      font-size: clamp(1.5rem, 3.5vw, 2.4rem) !important;\n'
        '      margin: 8px 0 16px;\n'
        '    }'
    )
    new_main_css = (
        '    #title-screen .main-title {\n'
        '      font-size: clamp(1.4rem, 3.2vw, 2.6rem) !important;\n'
        '      margin: 8px 0 4px !important;\n'
        '      text-transform: none !important;\n'
        '      letter-spacing: 2px !important;\n'
        f'      background: {gradient} !important;\n'
        '      -webkit-background-clip: text !important;\n'
        '      background-clip: text !important;\n'
        '      -webkit-text-fill-color: transparent !important;\n'
        f'      text-shadow: 0 0 40px {shadow} !important;\n'
        '    }\n'
        '    .mission-label {\n'
        '      font-family: \'Space Mono\', monospace;\n'
        '      font-size: 0.78em;\n'
        '      letter-spacing: 3px;\n'
        '      text-transform: uppercase;\n'
        f'      color: {color};\n'
        '      opacity: 0.6;\n'
        '      margin: 2px 0 22px;\n'
        '      text-align: center;\n'
        '    }\n'
        '    #title-screen .start-btn {\n'
        f'      border-color: {color} !important;\n'
        f'      color: {color} !important;\n'
        '    }\n'
        '    #title-screen .start-btn::before {\n'
        f'      background: linear-gradient(90deg,transparent,{rgba},0.3),transparent) !important;\n'
        '    }\n'
        '    #title-screen .start-btn:hover {\n'
        f'      background: {rgba},0.08) !important;\n'
        f'      box-shadow: 0 0 30px {rgba},0.5), inset 0 0 30px {rgba},0.08) !important;\n'
        '    }'
    )

    if old_main_css in content:
        content = content.replace(old_main_css, new_main_css, 1)
    else:
        # Try alternate format (some modules use different spacing)
        alt_old = (
            '    #title-screen .main-title {\n'
            '      font-size: clamp(1.5rem, 3.5vw, 2.4rem) !important;\n'
            '      margin: 8px 0 16px;\n'
            '    }\n'
        )
        if alt_old in content:
            content = content.replace(alt_old, new_main_css + '\n', 1)
        else:
            print(f"  WARNING {filename}: main-title CSS block not found")

    # ----------------------------------------------------------
    # 2. CSS: Add sidebar standardization before </style></head>
    # ----------------------------------------------------------
    sidebar_std = (
        '\n    /* === STANDARDISATION FORMAT SIDEBAR === */\n'
        '    .briefing-nav { width: 280px !important; }\n'
        '    .briefing-nav-item { padding: 15px 20px !important; font-size: 0.9em !important; }\n'
        '    .nav-icon { font-size: 1.2em !important; width: 28px !important; text-align: center !important; flex-shrink: 0 !important; }\n'
        '    .nav-number { font-family: \'Space Mono\', monospace !important; font-size: 0.75em !important; padding: 2px 6px !important; border-radius: 3px !important; min-width: 24px !important; text-align: center !important; flex-shrink: 0 !important; }\n'
        '    .briefing-title { font-size: 1.3em !important; }\n'
    )

    # Only add if not already present
    if 'STANDARDISATION FORMAT SIDEBAR' not in content:
        # Insert before the last </style> before </head>
        content = re.sub(
            r'(\n</style>\n</head>)',
            sidebar_std + r'\1',
            content,
            count=1
        )
        if 'STANDARDISATION FORMAT SIDEBAR' not in content:
            print(f"  WARNING {filename}: could not insert sidebar standardization CSS")

    # ----------------------------------------------------------
    # 3. HTML: Change module-official-label text to just number
    # ----------------------------------------------------------
    old_label_text = f'Module n° {num} : {mod_name}'
    new_label_text = f'Module n° {num}'
    if old_label_text in content:
        content = content.replace(old_label_text, new_label_text, 1)
    else:
        # Try alternate with accent/apostrophe variants
        # Use regex to find the pattern
        pattern = rf'Module n° {num} :[^<]+'
        match = re.search(pattern, content)
        if match:
            content = content[:match.start()] + f'Module n° {num}' + content[match.end():]
        else:
            print(f"  WARNING {filename}: module-official-label text not found")

    # ----------------------------------------------------------
    # 4. HTML: Change main-title h1 text to module name
    # ----------------------------------------------------------
    old_h1 = f'<h1 class="main-title">{old_title}</h1>'
    new_h1 = (
        f'<h1 class="main-title">{mod_name}</h1>\n'
        f'    <p class="mission-label">{mission_label}</p>'
    )
    if old_h1 in content:
        content = content.replace(old_h1, new_h1, 1)
    else:
        # Try without exact match (whitespace variations)
        pattern = r'<h1\s+class="main-title">' + re.escape(old_title) + r'</h1>'
        if re.search(pattern, content):
            content = re.sub(
                pattern,
                f'<h1 class="main-title">{mod_name}</h1>\n    <p class="mission-label">{mission_label}</p>',
                content,
                count=1
            )
        else:
            print(f"  WARNING {filename}: h1 main-title '{old_title}' not found")

    # ----------------------------------------------------------
    # 5. Guard: don't add mission-label twice
    # ----------------------------------------------------------
    # Already handled by replacing once above

    write(filename, content)


# Run for all modules
for (filename, mod_name, mission_label, num, color, rgba_base, old_title) in MODULES:
    path = os.path.join(BASE, filename)
    if os.path.exists(path):
        print(f"=== {filename} ===")
        fix_module(filename, mod_name, mission_label, num, color, rgba_base, old_title)
    else:
        print(f"  SKIP: {filename} not found")

print("\nAll done!")
