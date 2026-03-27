#!/usr/bin/env python3
"""
Harmonisation des titres de leçons dans les 15 modules :
1. Définir --domain-color là où elle est absente/incorrecte
2. Injecter un bloc CSS unifié pour .module-title / .lesson-title / .section-title :
   - font-size: 1.8em
   - font-weight: 700 (gras uniforme)
   - color: var(--domain-color)
   - padding-bottom, margin-bottom, border-bottom cohérents
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# Couleur thème par module (hex) — à définir en variable CSS si absente
MODULE_CONFIG = {
    'module-01-demystifier-ia.html':         {'color': '#ff6b6b', 'title_class': 'module-title'},
    'module1.html':                           {'color': '#ff6b6b', 'title_class': 'module-title'},
    'module-02-donnees-sous-influence.html':  {'color': '#ff6b6b', 'title_class': 'module-title'},
    'module-03-dans-la-tete-du-modele.html':  {'color': '#ff6b6b', 'title_class': 'lesson-title'},
    'module-04-generer-sans-comprendre.html': {'color': '#ff6b6b', 'title_class': 'lesson-title'},
    'module-05-art-de-la-consigne.html':      {'color': '#4ecdc4', 'title_class': 'section-title'},
    'module-06-iteration-amelioration.html':  {'color': '#00ff88', 'title_class': 'module-title'},
    'module-07-co-creer-ia.html':             {'color': '#4ecdc4', 'title_class': 'module-title'},
    'module-08-choisir-bon-usage.html':       {'color': '#4ecdc4', 'title_class': 'module-title'},
    'module-09-hallucinations.html':          {'color': '#ffe66d', 'title_class': 'module-title'},
    'module-10-biais-algorithmiques.html':    {'color': '#ffe66d', 'title_class': 'lesson-title'},
    'module-11-signal-falsifie.html':         {'color': '#ffe66d', 'title_class': 'module-title'},
    'module-12-impact-environnemental.html':  {'color': '#00ff88', 'title_class': 'module-title'},
    'module-13-vie-privee-donnees.html':      {'color': '#00ff88', 'title_class': 'module-title'},
    'module-14-ia-et-emploi.html':            {'color': '#00e5cc', 'title_class': 'module-title'},
    'module15-le-tribunal-de-l-ia.html':      {'color': '#00ff88', 'title_class': 'module-title'},
}

def hex_to_rgba_str(hex_color, alpha=0.3):
    """Convertit #rrggbb en 'r, g, b' pour rgba()"""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'

# Marqueur de fin du bloc de standardisation déjà injecté
# On injecte juste avant la fermeture du bloc standardisation
INJECT_MARKER = '/* FIN STANDARDISATION */'
INJECT_MARKER_ALT = '/* === FIN STANDARDISATION'

print("=== Harmonisation des titres de leçons ===\n")

for fname, cfg in MODULE_CONFIG.items():
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    color = cfg['color']
    title_class = cfg['title_class']
    border_color = hex_to_rgba_str(color, 0.3)

    # ── 1. Définir --domain-color si absente ou incorrecte ──────────────────
    # Chercher si --domain-color est définie dans :root ou dans le bloc standardisation
    has_domain_color = '--domain-color:' in content or '--domain-color :' in content

    # Trouver le bloc de standardisation injecté pour y ajouter --domain-color
    # Le bloc standardisation commence par un commentaire spécifique
    std_block_match = re.search(
        r'(/\* ={3,} STANDARDISATION[^*]*\*/)(.*?)(/\* ={0,}FIN STANDARDISATION[^*]*\*/)',
        content, re.DOTALL
    )

    if not std_block_match:
        # Chercher un autre marqueur possible
        std_block_match = re.search(
            r'(/\* ={3,} STANDARDISATION[^*]*\*/)(.*?)(/\* ={3,}[^*]*\*/)',
            content, re.DOTALL
        )

    # ── 2. Préparer le CSS de titre unifié ──────────────────────────────────
    # On utilisera les 3 classes pour couvrir tous les modules
    title_css = f"""
    /* Titres de leçons — harmonisation */
    .module-title, .lesson-title, .section-title {{
      font-size: 1.8em !important;
      font-weight: 700 !important;
      color: {color} !important;
      padding-bottom: 15px !important;
      margin-bottom: 25px !important;
      border-bottom: 1px solid {border_color} !important;
    }}"""

    # ── 3. Définir --domain-color si absente ────────────────────────────────
    domain_color_css = f"""
    /* Couleur thème du module */
    :root {{ --domain-color: {color}; }}"""

    # ── 4. Injecter dans le bloc standardisation ─────────────────────────────
    # Stratégie : trouver la fin du bloc style de standardisation et y insérer
    # On cherche le commentaire de fin, sinon on injecte avant </style>

    # Vérifier si les règles de titre sont déjà harmonisées
    already_done = (
        '.module-title, .lesson-title, .section-title' in content and
        'font-weight: 700 !important' in content
    )
    if already_done:
        print(f'✅ {fname} : titres déjà harmonisés')
        continue

    # Chercher le bloc de standardisation pour y injecter
    # Le bloc injecté lors de la phase précédente contient toujours .briefing-title
    # On cherche la fin de ce bloc (soit un commentaire FIN, soit la fermeture </style>
    # la plus proche après le début du bloc standardisation)

    std_start = content.find('/* === STANDARDISATION')
    if std_start == -1:
        std_start = content.find('/* STANDARDISATION')
    if std_start == -1:
        std_start = content.find('/* Standardisation')

    if std_start != -1:
        # Trouver la prochaine fermeture </style> après le début du bloc
        style_end = content.find('</style>', std_start)
        if style_end != -1:
            # Injecter juste avant </style>
            inject_point = style_end

            # Ajouter --domain-color si absent
            inject_content = ''
            if not has_domain_color:
                inject_content += domain_color_css + '\n'
            inject_content += title_css + '\n    '

            content = content[:inject_point] + inject_content + content[inject_point:]
        else:
            print(f'⚠  {fname} : </style> introuvable après bloc standardisation')
            continue
    else:
        # Pas de bloc standardisation trouvé — injecter dans le premier <style>
        style_end = content.find('</style>')
        if style_end != -1:
            inject_content = ''
            if not has_domain_color:
                inject_content += domain_color_css + '\n'
            inject_content += title_css + '\n    '
            content = content[:style_end] + inject_content + content[style_end:]
        else:
            print(f'⚠  {fname} : aucun bloc <style> trouvé')
            continue

    if content == original:
        print(f'⚠  {fname} : aucune modification effectuée')
        continue

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'✅ {fname} : couleur={color}')

print("\n✅ Terminé.")
