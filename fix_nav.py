#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove prev/next navigation bar from all module briefing sections.
The briefing-footer div with prev-btn/next-btn buttons is removed.
Also removes associated CSS that is only for the briefing-footer navigation.
"""

import re
import os

BASE = '/home/user/formationia'

FILES = [
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


def remove_briefing_footer(content):
    """
    Remove the briefing-footer div that contains prev/next navigation buttons.
    Handles various patterns across all 15 modules.
    Identifies navigation footers by presence of both "Précédent" and "Suivant" text
    (or prev-btn/next-btn/btn-prev/btn-next IDs) inside a briefing-footer div.
    """
    # Remove HTML comment + footer div block (module-01 style)
    content = re.sub(
        r'[ \t]*<!-- FOOTER WITH NAVIGATION -->[ \t]*\n[ \t]*<div class="briefing-footer">.*?</div>[ \t]*\n?',
        '',
        content, flags=re.DOTALL
    )

    # General approach: find all briefing-footer divs and remove those that
    # contain navigation buttons (any combination of prev/next button patterns)
    def should_remove_footer(div_content):
        """Return True if this briefing-footer contains navigation buttons."""
        nav_indicators = [
            'id="prev-btn"', 'id="next-btn"',
            'id="btn-prev"', 'id="btn-next"',
            'onclick="prevLesson()"', 'onclick="nextLesson()"',
            'onclick="prevSection()"', 'onclick="nextSection()"',
            '← Précédent', '← Fichier précédent', '← Dossier précédent',
            '← Section précédente', '← Cours précédent',
        ]
        return any(ind in div_content for ind in nav_indicators)

    # Match briefing-footer divs with their content
    def replace_footer(m):
        div_content = m.group(0)
        if should_remove_footer(div_content):
            return ''
        return div_content

    content = re.sub(
        r'[ \t]*<div class="briefing-footer">.*?</div>[ \t]*\n?',
        replace_footer,
        content, flags=re.DOTALL
    )

    return content


def remove_nav_js_dead_code(content):
    """
    Comment-mark (or remove) prevLesson/nextLesson functions if they exist
    and are only used by the removed buttons.
    These functions reference prev-btn and next-btn DOM elements.
    If we keep them, they'll just be unused dead code — OK to leave.
    Actually, we'll leave them to avoid breaking any potential references.
    """
    return content


def remove_briefing_footer_css(content):
    """
    Note: We leave the .briefing-footer CSS because some modules use it
    for other purposes (like the quiz footer). Only remove if it's
    clearly only for navigation.
    """
    return content


def process_file(filename):
    filepath = os.path.join(BASE, filename)
    print(f"Processing {filename} ...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = remove_briefing_footer(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Removed briefing footer")
    else:
        print(f"  - No briefing-footer found to remove")

    return content != original


if __name__ == '__main__':
    changed = 0
    for f in FILES:
        if process_file(f):
            changed += 1
    print(f"\nDone. {changed}/{len(FILES)} files updated.")
