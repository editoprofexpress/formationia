#!/usr/bin/env python3
"""
Ajoute un bouton "Lancer la mission" dans la section Mission des modules
12, 13, 14, 15 — et masque le briefing-footer sur tous les modules.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Bouton générique (domaine Enjeux Citoyens #95e1d3) ──────────────────────
def make_btn(fn, label):
    return (
        '\n        <div style="text-align:center;margin-top:30px;padding-bottom:20px">\n'
        f'            <button onclick="{fn}" style="font-family:\'Space Mono\',monospace;'
        'padding:16px 50px;background:rgba(149,225,211,0.15);border:2px solid var(--domain-color);'
        'color:var(--domain-color);cursor:pointer;font-size:1.1em;letter-spacing:2px;'
        'text-transform:uppercase;border-radius:6px;transition:all .3s" '
        'onmouseover="this.style.background=\'rgba(149,225,211,0.3)\'" '
        'onmouseout="this.style.background=\'rgba(149,225,211,0.15)\'">'
        f'{label}</button>\n'
        '        </div>'
    )

# ── Module 12 ────────────────────────────────────────────────────────────────
def fix_module12(content):
    old = (
        '                    <div class="module-section" style="text-align: center; padding-top: 20px;">\n'
        '                        <p style="font-size: 1.2em; color: var(--neon-green); margin-bottom: 20px;">\n'
        '                            🔐 Briefing terminé. Vous êtes prêt(e) pour l\'infiltration.\n'
        '                        </p>\n'
        '                    </div>'
    )
    btn = make_btn('startGame()', '🎮 Commencer l\'infiltration')
    new = (
        '                    <div class="module-section" style="text-align: center; padding-top: 20px;">\n'
        '                        <p style="font-size: 1.2em; color: var(--neon-green); margin-bottom: 20px;">\n'
        '                            🔐 Briefing terminé. Vous êtes prêt(e) pour l\'infiltration.\n'
        '                        </p>\n'
        f'{btn}\n'
        '                    </div>'
    )
    if old not in content:
        print("  ⚠ module-12 : marqueur introuvable, vérification manuelle nécessaire")
        return content
    return content.replace(old, new, 1)

# ── Module 13 ────────────────────────────────────────────────────────────────
def fix_module13(content):
    old = (
        '                    <p style="text-align:center; font-size:1.2em; color:var(--neon-green); margin-top:30px;">\n'
        '                        <strong>Prêt·e à protéger les données des citoyens ?</strong><br>\n'
        '                        Cliquez sur <strong>"Lancer la mission"</strong> ci-dessous !\n'
        '                    </p>'
    )
    btn = make_btn('startGame()', '🎮 Lancer la mission')
    new = (
        '                    <p style="text-align:center; font-size:1.2em; color:var(--neon-green); margin-top:30px;">\n'
        '                        <strong>Prêt·e à protéger les données des citoyens ?</strong><br>\n'
        '                        Prête à entrer en mission ?\n'
        '                    </p>\n'
        f'{btn}'
    )
    if old not in content:
        print("  ⚠ module-13 : marqueur introuvable, vérification manuelle nécessaire")
        return content
    return content.replace(old, new, 1)

# ── Module 14 ────────────────────────────────────────────────────────────────
def fix_module14(content):
    old = (
        '        <div class="divider"></div>\n'
        '        <p style="text-align:center;color:var(--muted);font-size:0.9em;">'
        'Cliquez sur <strong style="color:var(--neon-teal);">Ouvrir le bureau ARIA \u2192</strong>'
        ' pour commencer votre premi\u00e8re journ\u00e9e.</p>\n'
        '        `'
    )
    btn = make_btn('startARIA()', '⚙️ Ouvrir le bureau ARIA →')
    new = (
        '        <div class="divider"></div>\n'
        f'{btn}\n'
        '        `'
    )
    if old not in content:
        print("  ⚠ module-14 : marqueur introuvable, vérification manuelle nécessaire")
        return content
    return content.replace(old, new, 1)

# ── Module 15 ────────────────────────────────────────────────────────────────
def fix_module15(content):
    old = (
        '                    <div class="module-section" style="text-align: center; padding-top: 20px;">\n'
        '                        <p style="font-size: 1.2em; color: var(--neon-green); margin-bottom: 20px;">\n'
        '                            ⚖️ Briefing terminé. La séance est sur le point de commencer.\n'
        '                        </p>\n'
        '                    </div>'
    )
    btn = make_btn('startGame()', '⚖️ Entrer dans la salle d\'audience →')
    new = (
        '                    <div class="module-section" style="text-align: center; padding-top: 20px;">\n'
        '                        <p style="font-size: 1.2em; color: var(--neon-green); margin-bottom: 20px;">\n'
        '                            ⚖️ Briefing terminé. La séance est sur le point de commencer.\n'
        '                        </p>\n'
        f'{btn}\n'
        '                    </div>'
    )
    if old not in content:
        print("  ⚠ module-15 : marqueur introuvable, vérification manuelle nécessaire")
        return content
    return content.replace(old, new, 1)

# ── Masquage footer ───────────────────────────────────────────────────────────
FOOTER_CSS = '.briefing-footer{display:none!important}'
PROGRESS_CSS = '.briefing-progress{display:none!important}'

def hide_footer(content, filename):
    if FOOTER_CSS in content:
        print(f"  (footer déjà masqué)")
        return content
    # L'injecter juste après la ligne de masquage de la progress bar si elle existe
    if PROGRESS_CSS in content:
        return content.replace(PROGRESS_CSS, PROGRESS_CSS + '\n    ' + FOOTER_CSS, 1)
    # Sinon, l'injecter juste avant </style> dans le premier bloc <style>
    return content.replace('</style>', f'    {FOOTER_CSS}\n</style>', 1)

# ── Application ───────────────────────────────────────────────────────────────
MODULE_FIXES = {
    'module-12-impact-environnemental.html': fix_module12,
    'module-13-vie-privee-donnees.html':     fix_module13,
    'module-14-ia-et-emploi.html':           fix_module14,
    'module15-le-tribunal-de-l-ia.html':     fix_module15,
}

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

for fname in ALL_MODULES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f"⚠ Fichier introuvable : {fname}")
        continue

    print(f"📄 {fname}")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Masquer le footer
    content = hide_footer(content, fname)

    # 2. Ajouter le bouton mission si nécessaire
    if fname in MODULE_FIXES:
        print(f"  → Ajout bouton mission")
        content = MODULE_FIXES[fname](content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✅ Terminé.")
