#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to standardize title screens across all 15 Formation IA modules.
Changes:
  1. Fix back-link-title text: "Modules" → "Tous les modules"
  2. Add domain badge (colored) + "Module n° X : Official title" label
  3. Add activity type badge before start button
  4. Ensure Prof Express branding block is present
  5. Add CSS classes for new elements
"""

import re
import os

BASE = '/home/user/formationia'

MODULES = [
    {
        'key': '01',
        'file': 'module-01-demystifier-ia.html',
        'official_title': "Démystifier l'IA",
        'domain': 'Fondations IA',
        'domain_color': '#ff6b6b',
        'activity_type': '🎮 Mission d\'enquête',
    },
    {
        'key': '02',
        'file': 'module-02-donnees-sous-influence.html',
        'official_title': 'Données sous influence',
        'domain': 'Fondations IA',
        'domain_color': '#ff6b6b',
        'activity_type': '🎲 Jeu de simulation',
    },
    {
        'key': '03',
        'file': 'module-03-dans-la-tete-du-modele.html',
        'official_title': "Dans la tête d'un modèle",
        'domain': 'Fondations IA',
        'domain_color': '#ff6b6b',
        'activity_type': '🧠 Exploration interactive',
    },
    {
        'key': '04',
        'file': 'module-04-generer-sans-comprendre.html',
        'official_title': 'Générer sans comprendre',
        'domain': 'Fondations IA',
        'domain_color': '#ff6b6b',
        'activity_type': '🎮 Simulation',
    },
    {
        'key': '05',
        'file': 'module-05-art-de-la-consigne.html',
        'official_title': "L'art de la consigne",
        'domain': 'Interaction Raisonnée',
        'domain_color': '#4ecdc4',
        'activity_type': '🔐 Escape Room',
    },
    {
        'key': '06',
        'file': 'module-06-iteration-amelioration.html',
        'official_title': 'Itération et amélioration',
        'domain': 'Interaction Raisonnée',
        'domain_color': '#4ecdc4',
        'activity_type': '🎯 Défi progressif',
    },
    {
        'key': '07',
        'file': 'module-07-co-creer-ia.html',
        'official_title': "Co-créer avec l'IA",
        'domain': 'Interaction Raisonnée',
        'domain_color': '#4ecdc4',
        'activity_type': '🎨 Ateliers créatifs',
    },
    {
        'key': '08',
        'file': 'module-08-choisir-bon-usage.html',
        'official_title': 'Choisir le bon usage',
        'domain': 'Interaction Raisonnée',
        'domain_color': '#4ecdc4',
        'activity_type': '🧭 Triage de cas',
    },
    {
        'key': '09',
        'file': 'module-09-hallucinations.html',
        'official_title': "L'erreur qui sonne juste",
        'domain': 'Limites et Esprit Critique',
        'domain_color': '#ffe66d',
        'activity_type': '🔎 Enquête',
    },
    {
        'key': '10',
        'file': 'module-10-biais-algorithmiques.html',
        'official_title': 'Biais invisibles',
        'domain': 'Limites et Esprit Critique',
        'domain_color': '#ffe66d',
        'activity_type': "⚖️ Simulation d'audit",
    },
    {
        'key': '11',
        'file': 'module-11-signal-falsifie.html',
        'official_title': 'Signal Falsifié',
        'domain': 'Limites et Esprit Critique',
        'domain_color': '#ffe66d',
        'activity_type': '🎭 Investigation forensique',
    },
    {
        'key': '12',
        'file': 'module-12-impact-environnemental.html',
        'official_title': "Impact environnemental de l'IA",
        'domain': 'Enjeux Citoyens',
        'domain_color': '#95e1d3',
        'activity_type': '🔐 Escape Game',
    },
    {
        'key': '13',
        'file': 'module-13-vie-privee-donnees.html',
        'official_title': 'Données personnelles en danger',
        'domain': 'Enjeux Citoyens',
        'domain_color': '#95e1d3',
        'activity_type': '🎭 Jeu de rôle',
    },
    {
        'key': '14',
        'file': 'module-14-ia-et-emploi.html',
        'official_title': 'IA & Emploi — SHIFT',
        'domain': 'Enjeux Citoyens',
        'domain_color': '#95e1d3',
        'activity_type': '⚙️ Simulation de carrière',
    },
    {
        'key': '15',
        'file': 'module15-le-tribunal-de-l-ia.html',
        'official_title': 'Responsabilité humaine & IA',
        'domain': 'Enjeux Citoyens',
        'domain_color': '#95e1d3',
        'activity_type': '⚖️ Tribunal simulé',
    },
]

COMMON_CSS = """
    /* ==================== HARMONISATION TITRE (standardized) ==================== */
    .domain-badge-std {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 18px;
      border-radius: 20px;
      font-family: 'Space Mono', monospace;
      font-size: 0.75em;
      font-weight: 700;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 10px;
    }
    .module-official-label {
      font-family: 'Space Mono', monospace;
      font-size: 0.85em;
      color: #aabbcc;
      letter-spacing: 2px;
      margin-bottom: 15px;
      text-align: center;
      opacity: 0.9;
    }
    .activity-badge-std {
      display: inline-block;
      padding: 5px 16px;
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 14px;
      background: rgba(255,255,255,0.06);
      color: #aabbcc;
      font-size: 0.82em;
      margin-top: 12px;
      margin-bottom: 4px;
    }
    .profexpress-std {
      margin-top: 32px;
      opacity: 0.82;
      text-align: center;
    }
    .profexpress-std p {
      color: #8899aa;
      font-size: 0.8em;
      margin-bottom: 8px;
      letter-spacing: 1px;
      text-transform: uppercase;
    }
"""

PROFEXPRESS_BLOCK = """    <div class="profexpress-std">
      <p>Une formation proposée par</p>
      <a href="https://www.profexpress.com" target="_blank" rel="noopener">
        <img src="images/logo-profexpress.png" alt="Prof Express" style="height:32px;object-fit:contain;display:block;margin:0 auto;">
      </a>
    </div>"""


def add_css(content, css_to_add):
    """Insert new CSS before the closing </style> tag (first one). Skip if already added."""
    if 'HARMONISATION TITRE (standardized)' in content:
        return content  # already added in a previous run
    idx = content.find('</style>')
    if idx == -1:
        return content
    return content[:idx] + css_to_add + '\n' + content[idx:]


def fix_back_link_title(content):
    """Fix all back-link-title anchors to say 'Tous les modules'."""

    def replace_backlink(m):
        text = m.group(0)
        # Replace any variation of "Modules" (not preceded by "Tous les ")
        text = re.sub(r'(?<!Tous les )(?<!\w)Modules(?!\w)', 'Tous les modules', text)
        return text

    # Match the whole anchor tag with class back-link-title
    content = re.sub(
        r'<a[^>]*class="back-link-title"[^>]*>.*?</a>',
        replace_backlink,
        content,
        flags=re.DOTALL
    )
    return content


def fix_back_link_sidebar(content):
    """Fix sidebar back links to say 'Tous les modules'."""

    def replace_sidebar(m):
        text = m.group(0)
        text = re.sub(r'(?<!Tous les )(?<!\w)Modules(?!\w)', 'Tous les modules', text)
        return text

    content = re.sub(
        r'<a[^>]*class="back-link-sidebar"[^>]*>.*?</a>',
        replace_sidebar,
        content,
        flags=re.DOTALL
    )
    return content


def inject_domain_badge_and_label(content, meta):
    """
    After the back-link-title anchor, inject:
    - domain badge (colored)
    - module official label
    Skip if already injected (check in HTML body, not CSS).
    """
    # Check only in the body (after </style>) to avoid matching the CSS definition
    body_start = content.find('</style>')
    if body_start == -1:
        body_start = 0
    if 'domain-badge-std' in content[body_start:]:
        return content  # already injected in HTML

    color = meta['domain_color']
    domain = meta['domain']
    num = meta['key']
    official_title = meta['official_title']

    badge_html = (
        f'\n\n    <div class="domain-badge-std" style="background:{color}22;'
        f'border:1px solid {color}88;color:{color};">{domain}</div>\n'
        f'    <div class="module-official-label">Module n° {num} : {official_title}</div>'
    )

    # Insert after the back-link-title closing </a>
    # Find the back-link-title anchor and its closing tag
    pattern = r'(<a[^>]*class="back-link-title"[^>]*>.*?</a>)'
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        pos = match.end()
        content = content[:pos] + badge_html + content[pos:]

    return content


def inject_activity_badge(content, meta):
    """Inject activity type badge just before the start-btn button."""
    body_start = content.find('</style>')
    if body_start == -1:
        body_start = 0
    if 'activity-badge-std' in content[body_start:]:
        return content

    activity = meta['activity_type']
    badge = f'\n    <div class="activity-badge-std">{activity}</div>'

    # Insert before first start-btn
    content = re.sub(
        r'(\s*<button[^>]*class="start-btn")',
        badge + r'\1',
        content,
        count=1
    )
    return content


def ensure_profexpress(content):
    """
    Ensure Prof Express branding is present in the title screen.
    Only add if not already present INSIDE the title screen section.
    """
    # Find the title screen block
    ts_match = re.search(
        r'(<(?:section|div) id="title-screen"[^>]*>)(.*?)(?=\n\s*<!--\s*(?:=+\s*)?(?:BRIEFING|SECTION BRIEFING|ÉCRAN BRIEFING|GAME CON)|\n\s*<(?:section|div) id="briefing-screen")',
        content,
        flags=re.DOTALL
    )
    if not ts_match:
        return content

    ts_content = ts_match.group(2)

    # Check if branding already present
    if 'logo-profexpress' in ts_content or 'profexpress.com' in ts_content:
        # Still standardize the existing block
        # Replace old profexpress blocks with standardized one
        new_ts = re.sub(
            r'<div[^>]*(?:style="margin-top:\s*\d+px[^"]*"|class="profexpress[^"]*")[^>]*>\s*<p[^>]*>Une formation proposée par</p>\s*<a[^>]*profexpress\.com[^>]*>.*?</a>\s*</div>',
            PROFEXPRESS_BLOCK.strip(),
            ts_content,
            flags=re.DOTALL
        )
        if new_ts != ts_content:
            content = content[:ts_match.start(2)] + new_ts + content[ts_match.end(2):]
        return content

    # Add before the closing tag of title screen
    # Find the closing tag
    ts_end_match = re.search(
        r'(\s*</(?:section|div)>)\s*\n\s*<!--\s*(?:=+\s*)?(?:BRIEFING|SECTION BRIEFING|ÉCRAN BRIEFING)|\s*</(?:section|div)>\s*\n\s*<(?:section|div) id="briefing-screen"',
        content[ts_match.start():],
        flags=re.DOTALL
    )
    if ts_end_match:
        abs_pos = ts_match.start() + ts_end_match.start()
        content = content[:abs_pos] + '\n' + PROFEXPRESS_BLOCK + content[abs_pos:]

    return content


def remove_module_badge_old(content):
    """Remove/replace old module-badge div (like 'FONDATIONS IA — MODULE 04') if present."""
    # Old badge patterns like: <div class="module-badge">FONDATIONS IA — MODULE 04</div>
    # or <div class="domain-badge">Interaction Raisonnée · Module 7</div>
    # Remove these since we'll add standardized ones
    content = re.sub(
        r'\s*<div class="(?:module-badge|domain-badge)">[^<]*</div>',
        '',
        content
    )
    # Also remove old module-label or module-num-label if present from previous runs
    content = re.sub(
        r'\s*<div class="(?:module-label|module-num-label)">[^<]*</div>',
        '',
        content
    )
    return content


def process_module(meta):
    filepath = os.path.join(BASE, meta['file'])
    print(f"\nProcessing {meta['file']} ...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Add common CSS
    content = add_css(content, COMMON_CSS)

    # 2. Remove old non-standard domain/module badges
    content = remove_module_badge_old(content)

    # 3. Fix back-link-title text
    content = fix_back_link_title(content)

    # 4. Fix sidebar back-link-sidebar text
    content = fix_back_link_sidebar(content)

    # 5. Inject domain badge + official label after back-link-title
    content = inject_domain_badge_and_label(content, meta)

    # 6. Inject activity type badge before start button
    content = inject_activity_badge(content, meta)

    # 7. Ensure Prof Express branding
    content = ensure_profexpress(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    changed = content != original
    print(f"  {'✓ Updated' if changed else '- No changes'} ({len(content)} chars)")
    return changed


if __name__ == '__main__':
    changed_count = 0
    for meta in MODULES:
        if process_module(meta):
            changed_count += 1
    print(f"\n{'='*50}")
    print(f"Done. {changed_count}/{len(MODULES)} files updated.")
