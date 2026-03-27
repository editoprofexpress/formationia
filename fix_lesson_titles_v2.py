#!/usr/bin/env python3
"""
Correctifs titre de leçons — v2 :
1. Remplace color hardcodée par var(--domain-color) dans tous les modules
2. Ajoute --domain-color-border dans :root pour un border cohérent
3. Ajoute la numérotation (01 —, 02 —...) aux modules qui l'ont pas encore
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── Modules à renuméroter ────────────────────────────────────────────────────
# Tuples : (fichier, [(ancien_titre, nouveau_titre), ...])
# Pour les titres dans JS data array: format title:"..." ou title:'...'
# Pour les titres hardcodés HTML
NUMBERING_FIXES = {
    # ── M03 : hardcoded template literals ─────────────────────────────────────
    'module-03-dans-la-tete-du-modele.html': [
        ('🌐 Qu\'est-ce qu\'un modèle de langage ?', '01 — 🌐 Qu\'est-ce qu\'un modèle de langage ?'),
        ('⚙️ La Tokenisation',                       '02 — ⚙️ La Tokenisation'),
        ('🌌 Les Embeddings',                        '03 — 🌌 Les Embeddings'),
        ('🔍 Le Mécanisme d\'Attention',             '04 — 🔍 Le Mécanisme d\'Attention'),
        ('🎲 La Prédiction',                         '05 — 🎲 La Prédiction'),
        ('🚀 Mission NEURONAUTE',                    '06 — 🚀 Mission NEURONAUTE'),
    ],
    # ── M07 : hardcoded HTML ───────────────────────────────────────────────────
    'module-07-co-creer-ia.html': [
        ('🤝 L\'IA, partenaire créatif — pas un remplaçant', '01 — 🤝 L\'IA, partenaire créatif — pas un remplaçant'),
        ('✍️ Co-écrire avec l\'IA : texte, narration, style', '02 — ✍️ Co-écrire avec l\'IA : texte, narration, style'),
        ('🎨 Prompt visuel : l\'art de décrire l\'invisible',  '03 — 🎨 Prompt visuel : l\'art de décrire l\'invisible'),
        ('🎵 Musique et son génératif',                       '04 — 🎵 Musique et son génératif'),
        ('💻 Code assisté : l\'IA comme co-développeur',      '05 — 💻 Code assisté : l\'IA comme co-développeur'),
        ('⚖️ Droits d\'auteur, éthique et paternité créative','06 — ⚖️ Droits d\'auteur, éthique et paternité créative'),
    ],
    # ── M11 : template literals ────────────────────────────────────────────────
    'module-11-signal-falsifie.html': [
        ('📡 Qu\'est-ce qu\'un deepfake ?',                  '01 — 📡 Qu\'est-ce qu\'un deepfake ?'),
        ('🧠 Comment l\'IA fabrique-t-elle les faux ?',      '02 — 🧠 Comment l\'IA fabrique-t-elle les faux ?'),
        ('👁️ Détection visuelle — Les indices qui trahissent','03 — 👁️ Détection visuelle — Les indices qui trahissent'),
        ('🎤 Deepfakes Audio — La Voix Clonée',              '04 — 🎤 Deepfakes Audio — La Voix Clonée'),
        ('📰 Textes Deepfakes &amp; Désinformation',         '05 — 📰 Textes Deepfakes &amp; Désinformation'),
        ('⚠️ Impacts sur la Société',                        '06 — ⚠️ Impacts sur la Société'),
        ('🛡️ Se Protéger &amp; Vérifier',                   '07 — 🛡️ Se Protéger &amp; Vérifier'),
    ],
    # ── M12 : JS data array ────────────────────────────────────────────────────
    'module-12-impact-environnemental.html': [
        ('"🎬 Introduction : La Révolution de l\'IA Générative"', '"01 — 🎬 Introduction : La Révolution de l\'IA Générative"'),
        ('"🏢 Les Centres de Données : Cœur Énergétique de l\'IA"','"02 — 🏢 Les Centres de Données : Cœur Énergétique de l\'IA"'),
        ('"🌡️ L\'Empreinte Carbone du Numérique"',               '"03 — 🌡️ L\'Empreinte Carbone du Numérique"'),
        ('"💧 L\'Impact sur les Ressources en Eau"',              '"04 — 💧 L\'Impact sur les Ressources en Eau"'),
        ('"⛏️ L\'Extraction des Ressources Naturelles"',          '"05 — ⛏️ L\'Extraction des Ressources Naturelles"'),
        ('"🗑️ Les Déchets Électroniques"',                       '"06 — 🗑️ Les Déchets Électroniques"'),
        ('"🌱 Pistes pour une IA Plus Responsable"',              '"07 — 🌱 Pistes pour une IA Plus Responsable"'),
        ('"🎯 Briefing de Mission : Infiltration NovaTech"',      '"08 — 🎯 Briefing de Mission : Infiltration NovaTech"'),
    ],
    # ── M13 : JS data array ────────────────────────────────────────────────────
    'module-13-vie-privee-donnees.html': [
        ('"🎬 Introduction — Bienvenue chez SHIELD DATA"', '"01 — 🎬 Introduction — Bienvenue chez SHIELD DATA"'),
        ('"🔍 Qu\'est-ce qu\'une donnée personnelle ?"',   '"02 — 🔍 Qu\'est-ce qu\'une donnée personnelle ?"'),
        ('"🤖 IA & Collecte de données"',                '"03 — 🤖 IA & Collecte de données"'),
        ('"🇪🇺 Le RGPD et vos droits"',                  '"04 — 🇪🇺 Le RGPD et vos droits"'),
        ('"🍪 Cookies, trackers et empreinte numérique"', '"05 — 🍪 Cookies, trackers et empreinte numérique"'),
        ('"👁️ Surveillance et IA"',                      '"06 — 👁️ Surveillance et IA"'),
        ('"🛡️ Se protéger concrètement"',                '"07 — 🛡️ Se protéger concrètement"'),
        ('"🎮 Briefing de mission"',                     '"08 — 🎮 Briefing de mission"'),
    ],
    # ── M14 : hardcoded HTML template literals ─────────────────────────────────
    'module-14-ia-et-emploi.html': [
        ('🎬 Bienvenue à l\'Agence ARIA',           '01 — 🎬 Bienvenue à l\'Agence ARIA'),
        ('💥 Le Choc de l\'Automatisation',          '02 — 💥 Le Choc de l\'Automatisation'),
        ('⚠️ Les Métiers en Première Ligne',         '03 — ⚠️ Les Métiers en Première Ligne'),
        ('🤝 L\'IA Comme Collègue',                  '04 — 🤝 L\'IA Comme Collègue'),
        ('🚀 Les Nouveaux Métiers qui Émergent',     '05 — 🚀 Les Nouveaux Métiers qui Émergent'),
        ('🧠 Les Atouts Humains Irremplaçables',     '06 — 🧠 Les Atouts Humains Irremplaçables'),
        ('⚖️ Enjeux Sociaux et Politiques',          '07 — ⚖️ Enjeux Sociaux et Politiques'),
        ('🎯 Mission ARIA — Vos Clients vous Attendent', '08 — 🎯 Mission ARIA — Vos Clients vous Attendent'),
    ],
    # ── M15 : JS data array ────────────────────────────────────────────────────
    'module15-le-tribunal-de-l-ia.html': [
        ('"🧠 Introduction : Quand l\'IA prend des décisions"', '"01 — 🧠 Introduction : Quand l\'IA prend des décisions"'),
        ('"🔗 La Chaîne de Responsabilité"',                   '"02 — 🔗 La Chaîne de Responsabilité"'),
        ('"🤝 L\'éthique de l\'Intelligence Artificielle"',    '"03 — 🤝 L\'éthique de l\'Intelligence Artificielle"'),
        ('"🇪🇺 L\'AI Act : la loi européenne sur l\'IA"',     '"04 — 🇪🇺 L\'AI Act : la loi européenne sur l\'IA"'),
        ('"🌍 Et dans le reste du monde ?"',                   '"05 — 🌍 Et dans le reste du monde ?"'),
        ('"🧑‍⚖️ La supervision humaine : pourquoi c\'est essentiel"', '"06 — 🧑‍⚖️ La supervision humaine : pourquoi c\'est essentiel"'),
        ('"🧩 Construire une IA responsable"',                '"07 — 🧩 Construire une IA responsable"'),
        ('"🎯 Briefing de mission : Le Tribunal"',            '"08 — 🎯 Briefing de mission : Le Tribunal"'),
    ],
}

# ─── Corrections couleurs : remplacer hex par var(--domain-color) ─────────────
# Dans le bloc CSS injecté par fix_lesson_titles.py, remplacer toute couleur
# hardcodée par var(--domain-color) et corriger le border-bottom

ALL_FILES = [
    'module-01-demystifier-ia.html',
    'module1.html',
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

print("=== Correction couleurs + numérotation des titres ===\n")

for fname in ALL_FILES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # ── 1. Remplacer la couleur hardcodée par var(--domain-color) ────────────
    # Cibler uniquement le bloc CSS que l'on a injecté (repéré par le commentaire)
    old_color_block = re.search(
        r'(/\* Titres de leçons — harmonisation \*/\s*\.module-title.*?border-bottom:.*?!important;\s*\})',
        content, re.DOTALL
    )
    if old_color_block:
        old_block = old_color_block.group(1)
        # Remplacer la couleur hardcodée par var(--domain-color)
        new_block = re.sub(r'color: #[0-9a-fA-F]{6} !important;', 'color: var(--domain-color) !important;', old_block)
        # Remplacer le border rgba hardcodé par une variable
        new_block = re.sub(r'border-bottom: 1px solid rgba\([^)]+\) !important;',
                           'border-bottom: 1px solid var(--domain-color-border, rgba(255,255,255,0.15)) !important;', new_block)
        if new_block != old_block:
            content = content.replace(old_block, new_block)
            changes.append('couleur → var(--domain-color)')

    # ── 2. Ajouter --domain-color-border dans :root ───────────────────────────
    # On lit la valeur actuelle de --domain-color pour en déduire le border
    dc_match = re.search(r'--domain-color:\s*(#[0-9a-fA-F]{6})', content)
    if dc_match and '--domain-color-border' not in content:
        hex_c = dc_match.group(1).lstrip('#')
        r, g, b = int(hex_c[0:2],16), int(hex_c[2:4],16), int(hex_c[4:6],16)
        border_val = f'rgba({r}, {g}, {b}, 0.3)'
        # Ajouter --domain-color-border juste après --domain-color dans :root
        content = re.sub(
            r'(--domain-color:\s*#[0-9a-fA-F]{6};)',
            rf'\1\n  --domain-color-border: {border_val};',
            content, count=1
        )
        changes.append(f'--domain-color-border: {border_val}')

    # ── 3. Numérotation ──────────────────────────────────────────────────────
    if fname in NUMBERING_FIXES:
        for old_title, new_title in NUMBERING_FIXES[fname]:
            if old_title in content:
                content = content.replace(old_title, new_title)
                changes.append(f'"{old_title[:35]}..." → numéroté')
            # else: déjà corrigé ou absent

    if content == original:
        print(f'  {fname} : aucune modification')
    else:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ {fname}')
        for c in changes:
            print(f'   · {c}')

print("\n✅ Terminé.")
