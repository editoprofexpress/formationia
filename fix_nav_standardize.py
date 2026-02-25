#!/usr/bin/env python3
"""
Standardize sidebar nav items across all modules.
Fixes:
  1. Nav order: icon→text→number → icon→number→text (modules 03, 04, 11)
  2. Zero-pad single-digit numbers "1"→"01" (same modules)
  3. Module 05: add .nav-num to CSS override (class mismatch)
  4. Module 14: add number badges to nav items
  5. Add game/mission nav item in sidebar (modules 04, 05, 07, 08, 10)
  6. Fix separator div color to match domain (rgba(0,212,255,...) → correct)
  7. Module 11: fix game nav item order (icon→text→▶ → icon→▶→text)
"""

import re, os

BASE = '/home/user/formationia'

def read(fn):
    with open(os.path.join(BASE, fn), 'r', encoding='utf-8') as f:
        return f.read()

def write(fn, content):
    with open(os.path.join(BASE, fn), 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Saved {fn}")

# ============================================================
# FIX 1+2: Reorder nav items (icon→text→number → icon→number→text)
#           + zero-pad single-digit numbers
# ============================================================

def fix_nav_order(content):
    """
    Pattern: <span class="nav-icon">X</span>[ws]<span>TEXT</span>[ws]<span class="nav-number">N</span>
    Replace: <span class="nav-icon">X</span>[ws]<span class="nav-number">0N</span>[ws]TEXT
    Only matches spans where number content is digits 1-9 (not ▶ or --)
    """
    def replacer(m):
        pre_ws   = m.group(1)   # leading whitespace before icon
        icon_sp  = m.group(2)   # <span class="nav-icon">...</span>
        sep1     = m.group(3)   # whitespace between icon and text span
        text     = m.group(4).strip()
        sep2     = m.group(5)   # whitespace between text span and number span
        num      = m.group(6)   # digit(s)

        # Zero-pad
        num = str(int(num)).zfill(2)

        if '\n' in sep1:
            indent = sep1  # e.g. "\n        "
        elif '\n' in sep2:
            indent = sep2
        else:
            indent = ''   # same line

        if indent:
            return f'{pre_ws}{icon_sp}{indent}<span class="nav-number">{num}</span>{indent}{text}'
        else:
            return f'{pre_ws}{icon_sp}<span class="nav-number">{num}</span>{text}'

    pattern = (
        r'([ \t]*)'
        r'(<span class="nav-icon">[^<]+</span>)'    # icon span
        r'([ \t\n]*)'
        r'<span>([^<]+)</span>'                      # text span (plain <span>)
        r'([ \t\n]*)'
        r'<span class="nav-number">([0-9]+)</span>'  # number span (digits only)
    )
    return re.sub(pattern, replacer, content)

# ============================================================
# FIX 3: Module 05 — add .nav-num alongside .nav-number in CSS override
# ============================================================

def fix_mod05_navnum_css(content):
    old1 = '.nav-number { background: rgba(78,205,196,0.2) !important; }'
    new1 = '.nav-number, .nav-num { background: rgba(78,205,196,0.2) !important; }'
    old2 = '.briefing-nav-item.active .nav-number { background: rgba(78,205,196,0.4) !important; }'
    new2 = '.briefing-nav-item.active .nav-number, .briefing-nav-item.active .nav-num { background: rgba(78,205,196,0.4) !important; }'
    content = content.replace(old1, new1)
    content = content.replace(old2, new2)
    return content

# ============================================================
# FIX 4: Module 14 — add numbers and ▶ for game item
# ============================================================

MOD14_LESSONS = [
    (0, '🎬', 'Introduction'),
    (1, '💥', 'Le choc'),
    (2, '⚠️', 'Métiers à risque'),
    (3, '🤝', 'IA collègue'),
    (4, '🚀', 'Nouveaux métiers'),
    (5, '🧠', 'Atouts humains'),
    (6, '⚖️', 'Enjeux sociaux'),
]

def fix_mod14_numbers(content):
    for idx, icon, text in MOD14_LESSONS:
        num = str(idx + 1).zfill(2)
        old = f'<span class="nav-icon">{icon}</span> {text}'
        new = f'<span class="nav-icon">{icon}</span><span class="nav-number">{num}</span>{text}'
        if old in content:
            content = content.replace(old, new, 1)
        else:
            print(f"  WARNING mod14: pattern not found: {icon} {text}")
    # Game item nav-7: Mission ARIA
    old7 = '<span class="nav-icon">🎯</span> Mission ARIA'
    new7 = '<span class="nav-icon">🎯</span><span class="nav-number">▶</span>Mission ARIA'
    if old7 in content:
        content = content.replace(old7, new7, 1)
    else:
        print("  WARNING mod14: Mission ARIA pattern not found")
    return content

# ============================================================
# FIX 5+6: Add game nav item in separator + fix separator color
# For modules 04, 05, 07, 08 (all share same wrong separator rgba(0,212,255,0.2))
# ============================================================

WRONG_SEP_COLOR = 'rgba(0,212,255,0.2)'

def game_nav_html(onclick, icon, text, indent='          '):
    return (
        f'{indent}<div class="briefing-nav-item" id="game-nav-item" onclick="{onclick}">\n'
        f'{indent}  <span class="nav-icon">{icon}</span>\n'
        f'{indent}  <span class="nav-number">▶</span>\n'
        f'{indent}  {text}\n'
        f'{indent}</div>\n'
    )

def add_game_nav_wrong_color(content, onclick, icon, text, correct_color):
    """Insert game nav into the separator div that currently has wrong color."""
    game = game_nav_html(onclick, icon, text, indent='          ')
    old = (
        f'<div style="border-top:1px solid {WRONG_SEP_COLOR};margin-top:15px;padding-top:15px">\n'
        f'          <div class="briefing-nav-item" id="certificate-nav-item"'
    )
    new = (
        f'<div style="border-top:1px solid {correct_color};margin-top:15px;padding-top:15px">\n'
        f'{game}'
        f'          <div class="briefing-nav-item" id="certificate-nav-item"'
    )
    if old in content:
        content = content.replace(old, new, 1)
    else:
        print(f"  WARNING: separator pattern not found for {onclick}")
    return content

def add_game_nav_mod10(content):
    """Module 10 has correct yellow separator color, just insert game nav."""
    game = game_nav_html('launchGame()', '⚡', "Lancer l'audit", indent='        ')
    old = (
        '<div style="border-top:1px solid rgba(255,230,109,0.2);margin-top:15px;padding-top:15px">\n'
        '        <div class="briefing-nav-item" id="certificate-nav-item"'
    )
    new = (
        '<div style="border-top:1px solid rgba(255,230,109,0.2);margin-top:15px;padding-top:15px">\n'
        f'{game}'
        '        <div class="briefing-nav-item" id="certificate-nav-item"'
    )
    if old in content:
        content = content.replace(old, new, 1)
    else:
        print("  WARNING mod10: separator pattern not found")
    return content

# ============================================================
# FIX 7: Module 11 game nav item order (icon→text→▶ → icon→▶→text)
# ============================================================

def fix_mod11_game_nav_order(content):
    old = (
        '        <span class="nav-icon">🔍</span>\n'
        '        <span>Salle d\'analyse</span>\n'
        '        <span class="nav-number" id="game-nav-num">▶</span>'
    )
    new = (
        '        <span class="nav-icon">🔍</span>\n'
        '        <span class="nav-number" id="game-nav-num">▶</span>\n'
        '        Salle d\'analyse'
    )
    if old in content:
        content = content.replace(old, new, 1)
    else:
        print("  WARNING mod11: game nav item pattern not found")
    return content

# ============================================================
# MAIN
# ============================================================

print("=== Module 03: fix nav order ===")
c = read('module-03-dans-la-tete-du-modele.html')
c = fix_nav_order(c)
write('module-03-dans-la-tete-du-modele.html', c)

print("=== Module 04: fix nav order + add game nav + fix sep color ===")
c = read('module-04-generer-sans-comprendre.html')
c = fix_nav_order(c)
c = add_game_nav_wrong_color(c, 'launchGame()', '🤖', 'Lancer la simulation', 'rgba(255,107,107,0.2)')
write('module-04-generer-sans-comprendre.html', c)

print("=== Module 05: fix nav-num CSS + add game nav + fix sep color ===")
c = read('module-05-art-de-la-consigne.html')
c = fix_mod05_navnum_css(c)
c = add_game_nav_wrong_color(c, 'startGame()', '🔐', 'Entrer dans le Lab', 'rgba(78,205,196,0.2)')
write('module-05-art-de-la-consigne.html', c)

print("=== Module 07: add game nav + fix sep color ===")
c = read('module-07-co-creer-ia.html')
c = add_game_nav_wrong_color(c, 'startAtelier()', '🎨', 'Accéder aux ateliers', 'rgba(78,205,196,0.2)')
write('module-07-co-creer-ia.html', c)

print("=== Module 08: add game nav + fix sep color ===")
c = read('module-08-choisir-bon-usage.html')
c = add_game_nav_wrong_color(c, 'startTriage()', '🚦', 'Centre de Triage', 'rgba(78,205,196,0.2)')
write('module-08-choisir-bon-usage.html', c)

print("=== Module 10: add game nav ===")
c = read('module-10-biais-algorithmiques.html')
c = add_game_nav_mod10(c)
write('module-10-biais-algorithmiques.html', c)

print("=== Module 11: fix nav order + fix game nav order ===")
c = read('module-11-signal-falsifie.html')
c = fix_nav_order(c)
c = fix_mod11_game_nav_order(c)
write('module-11-signal-falsifie.html', c)

print("=== Module 14: add numbers ===")
c = read('module-14-ia-et-emploi.html')
c = fix_mod14_numbers(c)
write('module-14-ia-et-emploi.html', c)

print("\nAll done!")
