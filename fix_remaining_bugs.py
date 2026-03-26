#!/usr/bin/env python3
"""
Correctifs pour les bugs restants après la standardisation responsive :

1. Modules 3,4,5,7,8,10,11 : barre latérale visible sur mobile
   → Ajouter .briefing-nav{display:none!important} dans le bloc @media(max-width:768px)
   injecté par fix_responsive_nav.py

2. Modules 2,6,9 : bouton d'entrée ne fonctionne pas
   → Supprimer le doublon de template d'attestation (cause SyntaxError JS)

3. Module 1 : pas de menu burger
   → Ajouter .briefing-nav{display:none!important} + display:flex!important au media block
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ── Correctif 1 : ajouter display:none au sidebar dans le media block mobile ──
# Cible : les modules qui ont le bloc @media(max-width:768px){ .mobile-nav-bar{display:flex}... }
# mais PAS .briefing-nav{display:none} dans ce même bloc

MODULES_SIDEBAR_FIX = [
    'module1.html',
    'module-03-dans-la-tete-du-modele.html',
    'module-04-generer-sans-comprendre.html',
    'module-05-art-de-la-consigne.html',
    'module-07-co-creer-ia.html',
    'module-08-choisir-bon-usage.html',
    'module-10-biais-algorithmiques.html',
    'module-11-signal-falsifie.html',
]

# Le bloc cible a été injecté par fix_responsive_nav.py et ressemble à :
# @media(max-width:768px){
#   .mobile-nav-bar{display:flex}
#   .briefing-nav.nav-open{display:flex!important;...}
#   ...
# }
# On veut ajouter .briefing-nav{display:none!important} juste après .mobile-nav-bar{display:flex}

OLD_NAV_LINE = '.mobile-nav-bar{display:flex}'
NEW_NAV_LINE = '.mobile-nav-bar{display:flex!important}\n      .briefing-nav{display:none!important}'

print("=== Correctif 1 : masquage sidebar sur mobile ===")
for fname in MODULES_SIDEBAR_FIX:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier si la ligne cible existe dans le bon contexte (après mobile-nav-bar CSS)
    # On cherche le pattern dans le bloc @media(max-width:768px) contenant mobile-nav-bar
    # On vérifie d'abord si la correction est déjà présente
    if 'briefing-nav{display:none!important}' in content and OLD_NAV_LINE.replace('flex}', 'flex!important}') in content:
        print(f'✅ {fname} déjà corrigé')
        continue

    if OLD_NAV_LINE not in content:
        print(f'⚠  {fname}: marqueur introuvable')
        continue

    # Remplacer uniquement la première occurrence dans le bloc mobile (après les CSS nav mobile)
    # On recherche spécifiquement dans le contexte du bloc @media injecté
    updated = content.replace(OLD_NAV_LINE, NEW_NAV_LINE, 1)

    if updated == content:
        print(f'⚠  {fname}: aucune modification effectuée')
        continue

    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated)

    has_fix = 'briefing-nav{display:none!important}' in updated
    print(f'{"✅" if has_fix else "⚠"} {fname}')

print()

# ── Correctif 2 : supprimer le doublon de template d'attestation ──────────────
# Les modules 2, 6, 9 ont une duplication du template HTML dans downloadCertificate()
# Le premier template se ferme avec `</body></html>\`;`
# Puis le second template commence avec `</style></head><body>...` (hors template literal)
# Cela cause un SyntaxError JS qui casse TOUTES les fonctions du module.

MODULES_CERT_FIX = [
    'module-02-donnees-sous-influence.html',
    'module-06-iteration-amelioration.html',
    'module-09-hallucinations.html',
]

print("=== Correctif 2 : suppression doublon template attestation ===")
for fname in MODULES_CERT_FIX:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'⚠  {fname} introuvable'); continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern : le premier template se ferme à </body></html>`;
    # Puis la ligne suivante commence un doublon HTML qui se termine par </body></html>`;
    # On veut supprimer tout ce qui est entre le premier `; et la fin du deuxième template `;
    # mais GARDER le premier (mettre à jour le programme pour "Fondamentaux et usages...")

    # Plus précisément : trouver la séquence
    # </body></html>`;
    # </style></head><body>...contenu doublon...</body></html>`;
    # Et supprimer la deuxième ligne (le doublon)

    # Regex : après la fermeture du premier template, supprimer le contenu orphelin
    # Le doublon commence par </style> ou </head> après la fermeture du premier backtick
    pattern = r'(</body></html>`;\n)</style></head><body>[^\n]+\n'

    match = re.search(pattern, content)
    if not match:
        # Essayer un pattern alternatif (une seule longue ligne)
        pattern2 = r'(</body></html>`;)\n</style></head><body>[^`]+`;\n'
        match = re.search(pattern2, content, re.DOTALL)
        if not match:
            print(f'⚠  {fname}: doublon introuvable, vérification manuelle')
            continue
        updated = content[:match.start()] + match.group(1) + '\n' + content[match.end():]
    else:
        updated = re.sub(pattern, r'\1', content, count=1)

    # Mettre à jour le programme dans le premier template : "IA Responsable" → "Fondamentaux..."
    updated = updated.replace(
        '<div class="sub">Formation IA Responsable</div>',
        '<div class="sub">Fondamentaux et usages de l\'intelligence artificielle</div>',
        1
    )
    # Aussi dans le .fv (Programme footer de l'attestation)
    updated = updated.replace(
        '<div class="fv">IA Responsable</div>',
        '<div class="fv">Fondamentaux et usages de l\'IA</div>',
        1
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(updated)

    # Vérifier qu'il ne reste plus de contenu orphelin
    remaining = re.search(r'</body></html>`;\n</style>', updated)
    print(f'{"✅" if not remaining else "⚠"} {fname} [doublon {"supprimé" if not remaining else "TOUJOURS PRÉSENT"}]')

print()
print("✅ Terminé.")
