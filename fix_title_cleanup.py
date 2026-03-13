#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean up title screens across all 15 modules.

Uses depth-aware div removal to handle nested div structures correctly.

Changes:
1. Update .module-official-label CSS to be more prominent
2. Add #title-screen .main-title CSS override (smaller game title)
3. Remove <p class="subtitle"> / <div class="subtitle"> duplicates
4. Remove stats panels: module-info, mission-stats, title-stats, quick-stats, stats-row
5. Remove ticker-wrap (module 10)
6. Remove terminal-line divs (modules 04, 05)
7. Remove module-tag divs (module 11)
8. Simplify intro-box: remove wrapper + dispatch-header, keep <p> narratives
9. Simplify mission-card (module 10): remove wrapper + label, keep narrative text
10. Remove title-content wrapper (module 10) keeping its content
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


# ─────────────────────────────────────────────────────────────────────────────
# Depth-aware div utilities
# ─────────────────────────────────────────────────────────────────────────────

def find_matching_close_div(text, open_pos):
    """
    Given position of '<div...' opening, find position just AFTER its matching '</div>'.
    Returns -1 if not found.
    """
    depth = 0
    pos = open_pos
    length = len(text)
    while pos < length:
        next_open = text.find('<div', pos)
        next_close = text.find('</div>', pos)

        if next_close == -1:
            return -1

        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            if depth <= 1:
                # This </div> closes the outermost div we're tracking
                return next_close + len('</div>')
            depth -= 1
            pos = next_close + 6

    return -1


def remove_divs_by_class(content, class_name):
    """
    Remove ALL <div class="CLASS_NAME"> elements (with their nested content).
    Also strips leading whitespace on the same line and trailing newline.
    """
    search = f'<div class="{class_name}">'
    while True:
        idx = content.find(search)
        if idx == -1:
            break

        # Find start of the line (to remove leading whitespace too)
        line_start = content.rfind('\n', 0, idx)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1  # include the newline char itself in removal? No, keep \n before

        # Find end of the entire div block
        end = find_matching_close_div(content, idx)
        if end == -1:
            break  # malformed HTML, skip

        # Remove trailing newline after the closing tag
        if end < len(content) and content[end] == '\n':
            end += 1

        # Remove from start of leading whitespace to end
        content = content[:line_start] + content[end:]

    return content


def get_div_inner_content(content, class_name):
    """
    Return the inner content of the FIRST <div class="CLASS_NAME"> element.
    Returns empty string if not found.
    """
    search = f'<div class="{class_name}">'
    idx = content.find(search)
    if idx == -1:
        return ''

    inner_start = idx + len(search)
    end = find_matching_close_div(content, idx)
    if end == -1:
        return ''

    # inner content is between end of opening tag and start of closing </div>
    inner_end = content.rfind('</div>', inner_start, end)
    return content[inner_start:inner_end]


def unwrap_div(content, class_name):
    """
    Remove the outer <div class="CLASS_NAME"> wrapper but keep its inner content.
    """
    search = f'<div class="{class_name}">'
    while True:
        idx = content.find(search)
        if idx == -1:
            break

        inner_start = idx + len(search)
        end = find_matching_close_div(content, idx)
        if end == -1:
            break

        inner_end = content.rfind('</div>', inner_start, end)
        inner_content = content[inner_start:inner_end]

        # Find start of line for whitespace cleanup
        line_start = content.rfind('\n', 0, idx)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1

        # Remove trailing newline after closing tag
        after = end
        if after < len(content) and content[after] == '\n':
            after += 1

        content = content[:line_start] + inner_content + content[after:]
        break  # only unwrap first occurrence (call again for more)

    return content


# ─────────────────────────────────────────────────────────────────────────────
# 1. CSS UPDATE
# ─────────────────────────────────────────────────────────────────────────────

NEW_LABEL_CSS = """    .module-official-label {
      font-family: 'Space Mono', monospace;
      font-size: 1.1em;
      color: #ffffff;
      font-weight: 600;
      letter-spacing: 1.5px;
      margin-bottom: 12px;
      text-align: center;
      opacity: 1;
    }
    #title-screen .main-title {
      font-size: clamp(1.5rem, 3.5vw, 2.4rem) !important;
      margin: 8px 0 16px;
    }"""


def update_css(content):
    """Replace .module-official-label block and add #title-screen .main-title override."""
    if '#title-screen .main-title' in content:
        return content  # already updated

    content = re.sub(
        r'[ \t]*\.module-official-label\s*\{[^}]+\}',
        lambda m: NEW_LABEL_CSS,
        content
    )
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 2. REMOVE SUBTITLE DUPLICATES
# ─────────────────────────────────────────────────────────────────────────────

def remove_subtitles(content):
    """Remove <p class="subtitle"> and <div class="subtitle"> lines."""
    content = re.sub(
        r'[ \t]*<(?:p|div) class="subtitle">[^\n]*\n?',
        '',
        content
    )
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 3. REMOVE STATS PANELS (using depth-aware removal)
# ─────────────────────────────────────────────────────────────────────────────

def remove_stats_panels(content):
    """Remove all stats/duration/info divs using depth-aware removal."""
    for cls in ['module-info', 'mission-stats', 'title-stats', 'quick-stats', 'stats-row']:
        content = remove_divs_by_class(content, cls)
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 4. REMOVE TICKER
# ─────────────────────────────────────────────────────────────────────────────

def remove_ticker(content):
    """Remove ticker-wrap div (module 10)."""
    # Remove optional HTML comment before ticker
    content = re.sub(r'[ \t]*<!-- Ticker[^>]*-->\s*\n?', '', content)
    content = remove_divs_by_class(content, 'ticker-wrap')
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 5. REMOVE TERMINAL LINES
# ─────────────────────────────────────────────────────────────────────────────

def remove_terminal_lines(content):
    """Remove terminal-line divs (modules 04, 05)."""
    # Remove optional comment before terminal-line
    content = re.sub(r'[ \t]*<!-- Ligne terminal[^>]*-->\s*\n?', '', content)
    content = remove_divs_by_class(content, 'terminal-line')
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 6. REMOVE MODULE-TAG
# ─────────────────────────────────────────────────────────────────────────────

def remove_module_tag(content):
    """Remove module-tag div (module 11) - single-line div."""
    content = re.sub(
        r'[ \t]*<div class="module-tag">[^\n]*\n?',
        '',
        content
    )
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 7. SIMPLIFY INTRO-BOX (modules 07, 08)
# ─────────────────────────────────────────────────────────────────────────────

def simplify_intro_box(content):
    """
    For modules with intro-box:
    - Remove dispatch-header div
    - Extract <p> narrative paragraphs
    - Remove mission-stats (already removed, but just in case)
    - Replace the whole intro-box with plain <p class="intro-text"> paragraphs
    """
    search = '<div class="intro-box">'
    idx = content.find(search)
    if idx == -1:
        return content

    inner_start = idx + len(search)
    end = find_matching_close_div(content, idx)
    if end == -1:
        return content

    inner_end = content.rfind('</div>', inner_start, end)
    inner = content[inner_start:inner_end]

    # Remove dispatch-header
    inner = remove_divs_by_class(inner, 'dispatch-header')
    # Remove any remaining mission-stats
    inner = remove_divs_by_class(inner, 'mission-stats')

    # Extract <p> contents (may have attributes or be multi-line)
    paras = re.findall(r'<p(?:[^>]*)>(.*?)</p>', inner, flags=re.DOTALL)

    if paras:
        replacement = '\n'.join(
            f'  <p class="intro-text">{p.strip()}</p>'
            for p in paras if p.strip()
        )
    else:
        replacement = ''

    # Find start of line for intro-box (for whitespace)
    line_start = content.rfind('\n', 0, idx)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    after = end
    if after < len(content) and content[after] == '\n':
        after += 1

    content = content[:line_start] + ('\n' + replacement + '\n' if replacement else '') + content[after:]
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 8. SIMPLIFY MISSION-CARD (module 10)
# ─────────────────────────────────────────────────────────────────────────────

def simplify_mission_card(content):
    """
    Remove mission-card wrapper + mission-label div,
    keep the narrative text as <p class="intro-text">.
    """
    search = '<div class="mission-card">'
    idx = content.find(search)
    if idx == -1:
        return content

    inner_start = idx + len(search)
    end = find_matching_close_div(content, idx)
    if end == -1:
        return content

    inner_end = content.rfind('</div>', inner_start, end)
    inner = content[inner_start:inner_end]

    # Remove mission-label
    inner = remove_divs_by_class(inner, 'mission-label')

    # Clean up text
    text = inner.strip()
    text = re.sub(r'<br\s*/?>\s*<br\s*/?>', ' ', text)
    text = re.sub(r'<br\s*/?>', ' ', text)
    text = text.strip()

    line_start = content.rfind('\n', 0, idx)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    after = end
    if after < len(content) and content[after] == '\n':
        after += 1

    replacement = f'  <p class="intro-text">{text}</p>' if text else ''
    content = content[:line_start] + ('\n' + replacement + '\n' if replacement else '') + content[after:]
    return content


# ─────────────────────────────────────────────────────────────────────────────
# 9. UNWRAP TITLE-CONTENT (module 10)
# ─────────────────────────────────────────────────────────────────────────────

def unwrap_title_content(content):
    """Remove the title-content wrapper div in module 10, keeping inner elements."""
    return unwrap_div(content, 'title-content')


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def process_file(filename):
    filepath = os.path.join(BASE, filename)
    print(f"\nProcessing {filename} ...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    content = update_css(content)
    content = remove_subtitles(content)
    content = remove_stats_panels(content)
    content = remove_ticker(content)
    content = remove_terminal_lines(content)
    content = remove_module_tag(content)
    content = simplify_intro_box(content)
    content = simplify_mission_card(content)
    content = unwrap_title_content(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        diff = len(content) - len(original)
        print(f"  ✓ Updated ({len(original)} → {len(content)} chars, {diff:+d})")
    else:
        print(f"  - No changes needed")

    return content != original


if __name__ == '__main__':
    changed = 0
    for f in FILES:
        if process_file(f):
            changed += 1
    print(f"\nDone. {changed}/{len(FILES)} files updated.")
