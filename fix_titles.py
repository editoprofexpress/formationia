#!/usr/bin/env python3
"""
Met à jour les balises <title> des modules pour le format :
"Module n°X — [thème]"
Seule la première balise <title> de chaque fichier est modifiée
(les titres des popups d'attestation sont laissés intacts).
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

TITLES = {
    'module1.html':                        'Module n°1 — Démystifier l\'IA',
    'module-01-demystifier-ia.html':       'Module n°1 — Démystifier l\'IA',
    'module-02-donnees-sous-influence.html':'Module n°2 — Données & Apprentissage',
    'module-03-dans-la-tete-du-modele.html':'Module n°3 — Dans la tête d\'un modèle',
    'module-04-generer-sans-comprendre.html':'Module n°4 — Générer sans comprendre',
    'module-05-art-de-la-consigne.html':   'Module n°5 — L\'Art de la consigne',
    'module-06-iteration-amelioration.html':'Module n°6 — Itération & Amélioration',
    'module-07-co-creer-ia.html':          'Module n°7 — Co-créer avec l\'IA',
    'module-08-choisir-bon-usage.html':    'Module n°8 — Choisir le bon usage',
    'module-09-hallucinations.html':       'Module n°9 — Hallucinations de l\'IA',
    'module-10-biais-algorithmiques.html': 'Module n°10 — Biais algorithmiques',
    'module-11-signal-falsifie.html':      'Module n°11 — Détection de deepfakes',
    'module-12-impact-environnemental.html':'Module n°12 — IA & Environnement',
    'module-13-vie-privee-donnees.html':   'Module n°13 — IA & Vie privée',
    'module-14-ia-et-emploi.html':         'Module n°14 — IA & Emploi',
    'module15-le-tribunal-de-l-ia.html':   'Module n°15 — Responsabilité humaine',
}

for fname, new_title in TITLES.items():
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠ Introuvable : {fname}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remplace seulement la première balise <title>...</title>
    updated, n = re.subn(r'<title>[^<]*</title>', f'<title>{new_title}</title>', content, count=1)
    if n:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f'✅ {fname}  →  {new_title}')
    else:
        print(f'⚠ Balise <title> introuvable : {fname}')

print('\n✅ Terminé.')
