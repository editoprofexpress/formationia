#!/usr/bin/env python3
"""
Deux correctifs :
1. Ajouter le logo/icône (::before) dans .briefing-title pour les modules qui n'en ont pas
2. Corriger le max-width du .briefing-content du module 3 (880px → 100%)
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# Icônes à ajouter pour les modules qui n'en ont pas
MODULE_ICONS = {
    'module-02-donnees-sous-influence.html':  '🧬',  # laboratoire / données
    'module-03-dans-la-tete-du-modele.html':  '🧠',  # cerveau / modèle
    'module-04-generer-sans-comprendre.html': '🎭',  # générer / créer
    'module-06-iteration-amelioration.html':  '✨',  # amélioration
    'module-09-hallucinations.html':          '👁️',  # perception / hallucination
    'module-10-biais-algorithmiques.html':    '⚡',  # algorithme / biais
    'module-11-signal-falsifie.html':         '📡',  # signal / détection
}

# Point d'injection : juste après la règle .briefing-title { font-size: 1.3em !important; }
# dans la section standardisation
INJECT_AFTER = '.briefing-title { font-size: 1.3em !important; }'
# Format de la règle ::before (même style que les modules existants)
BEFORE_TPL = "\n    .briefing-title::before {{ content: '{icon}'; font-size: 1.5em; }}"

print("=== Ajout des icônes manquantes ===\n")

for fname, icon in MODULE_ICONS.items():
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier si ::before est déjà présent
    if '.briefing-title::before' in content:
        print(f'✅ {fname} : icône déjà présente')
        continue

    # Injecter la règle ::before juste après la règle font-size dans la section standardisation
    before_rule = BEFORE_TPL.format(icon=icon)
    if INJECT_AFTER in content:
        updated = content.replace(INJECT_AFTER, INJECT_AFTER + before_rule, 1)
    else:
        # Fallback : injecter avant </style> (première occurrence dans <head>)
        # On cherche la fermeture du bloc standardisation
        alt_marker = '.briefing-title { font-size: 1.3em !important;}'
        alt2 = '.briefing-title{font-size:1.3em!important}'
        if alt_marker in content:
            updated = content.replace(alt_marker, alt_marker + before_rule, 1)
        elif alt2 in content:
            updated = content.replace(alt2, alt2 + before_rule, 1)
        else:
            # Injecter avant la fin du premier bloc <style>
            updated = content.replace('</style>', before_rule + '\n</style>', 1)

    if updated == content:
        print(f'⚠  {fname} : impossible d\'injecter')
        continue

    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated)
    print(f'✅ {fname} : icône {icon} ajoutée')

print()
print("=== Correctif max-width module 3 ===\n")

mod3 = os.path.join(BASE, 'module-03-dans-la-tete-du-modele.html')
with open(mod3, 'r', encoding='utf-8') as f:
    content = f.read()

# Remplacer max-width: 880px dans la règle .briefing-content originale
updated = re.sub(
    r'(\.briefing-content\s*\{[^}]*?)max-width\s*:\s*880px',
    r'\1max-width: 100%',
    content,
    count=1
)

if updated != content:
    with open(mod3, 'w', encoding='utf-8') as f:
        f.write(updated)
    print('✅ module-03 : max-width 880px → 100%')
else:
    print('⚠  module-03 : max-width 880px introuvable')

print("\n✅ Terminé.")
