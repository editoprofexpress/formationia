#!/usr/bin/env python3
"""
Harmonisation des en-têtes de tous les modules :
1. Remplace le contenu de .briefing-title par "Module n°X — Thème" (même format que le <title>)
2. Corrige les incohérences de capitalisation et de style dans les <title>
3. Supprime la jauge de progression du header du module 10 (et 14)
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Noms officiels standardisés ─────────────────────────────────────────────
# Format : "Module n°X — Thème"
# Règle : seul le premier mot (ou sigle) prend la majuscule, pas de & → "et"
MODULES = [
    ('module-01-demystifier-ia.html',         'Module n°1 — Démystifier l\'IA'),
    ('module1.html',                           'Module n°1 — Démystifier l\'IA'),
    ('module-02-donnees-sous-influence.html',  'Module n°2 — Données sous influence'),
    ('module-03-dans-la-tete-du-modele.html',  'Module n°3 — Dans la tête d\'un modèle'),
    ('module-04-generer-sans-comprendre.html', 'Module n°4 — Générer sans comprendre'),
    ('module-05-art-de-la-consigne.html',      'Module n°5 — L\'art de la consigne'),
    ('module-06-iteration-amelioration.html',  'Module n°6 — Itération et amélioration'),
    ('module-07-co-creer-ia.html',             'Module n°7 — Co-créer avec l\'IA'),
    ('module-08-choisir-bon-usage.html',       'Module n°8 — Choisir le bon usage'),
    ('module-09-hallucinations.html',          'Module n°9 — Hallucinations de l\'IA'),
    ('module-10-biais-algorithmiques.html',    'Module n°10 — Biais algorithmiques'),
    ('module-11-signal-falsifie.html',         'Module n°11 — Détection de deepfakes'),
    ('module-12-impact-environnemental.html',  'Module n°12 — IA et environnement'),
    ('module-13-vie-privee-donnees.html',      'Module n°13 — IA et vie privée'),
    ('module-14-ia-et-emploi.html',            'Module n°14 — IA et emploi'),
    ('module15-le-tribunal-de-l-ia.html',      'Module n°15 — Responsabilité humaine'),
]

print("=== Harmonisation des en-têtes ===\n")

for fname, new_name in MODULES:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # ── 1. Mettre à jour le <title> ──────────────────────────────────────────
    content = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_name}</title>',
        content, count=1
    )

    # ── 2. Remplacer le contenu de .briefing-title ───────────────────────────
    # Le div peut contenir : texte simple, emoji + texte, span + texte, etc.
    # On remplace tout le contenu entre > et </div>

    # Cas A : div inline sur une ligne : <div class="briefing-title">TEXTE</div>
    content, n_a = re.subn(
        r'(<div[^>]*class="briefing-title"[^>]*>)[^<]*(<\/div>)',
        lambda m: m.group(1) + new_name + m.group(2),
        content
    )

    # Cas B : div multi-ligne avec span ou texte sur plusieurs lignes
    if n_a == 0:
        content, n_b = re.subn(
            r'(<div[^>]*class="briefing-title"[^>]*>)(.*?)(<\/div>)',
            lambda m: m.group(1) + new_name + m.group(3),
            content,
            flags=re.DOTALL
        )
        replaced = n_b > 0
    else:
        replaced = True

    # ── 3. Suppression du ::before emoji sur .briefing-title (module 10) ─────
    # Module 10 a .briefing-title::before{content:'📋'...} → on retire l'icône
    # pour ne pas avoir doublon visuel (le texte se suffit à lui-même)
    content = re.sub(
        r'\s*\.briefing-title::before\{content:[^}]+\}\s*',
        '\n    ',
        content
    )

    # ── 4. Supprimer la jauge du header (modules 10 et 14) ───────────────────
    # Module 10 : <div class="briefing-progress-wrap">...</div>
    # → changer en "briefing-progress" pour que la règle display:none s'applique
    content = re.sub(
        r'class="briefing-progress-wrap"',
        'class="briefing-progress"',
        content
    )
    # Module 14 : <span id="lesson-counter">1 / 7</span> est dans briefing-progress
    # → déjà caché par .briefing-progress{display:none!important} global

    # ── 5. Retirer le CSS .briefing-title-icon si présent (module 11) ─────────
    # L'icône était dans un <span class="briefing-title-icon"> à l'intérieur du div
    # On l'a déjà retiré en remplaçant le contenu du div ci-dessus

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'✅ {fname}')
        print(f'   → {new_name}')
    else:
        print(f'⚠  {fname} : aucune modification')

print("\n✅ Terminé.")
