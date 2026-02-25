#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix JavaScript references to removed prev-btn/next-btn/btn-prev/btn-next elements.
After removing the briefing-footer HTML, the JS that updates these buttons
will throw TypeErrors. We add null checks or replace problematic code.
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

# Patterns to make safe with null checks
JS_FIXES = [
    # Pattern: document.getElementById('prev-btn').disabled = ...;
    # Fix: const _pb = document.getElementById('prev-btn'); if (_pb) _pb.disabled = ...;
    (
        r"document\.getElementById\('prev-btn'\)\.disabled\s*=\s*([^;]+);",
        r"{ const _pb = document.getElementById('prev-btn'); if (_pb) _pb.disabled = \1; }"
    ),
    (
        r"document\.getElementById\(\"prev-btn\"\)\.disabled\s*=\s*([^;]+);",
        r'{ const _pb = document.getElementById("prev-btn"); if (_pb) _pb.disabled = \1; }'
    ),
    # Pattern: const nextBtn = document.getElementById('next-btn');
    # then nextBtn.xxx → nextBtn might be null
    # We'll replace the whole block using a different approach
]


def fix_btn_references(content):
    """Add null-safety to button references in JavaScript."""

    # 1. Safe-guard direct .disabled = assignments on removed buttons
    content = re.sub(
        r"(\$\('prev-btn'\)|document\.getElementById\('prev-btn'\))\.disabled\s*=\s*([^;]+);",
        r"{ const _pb = \1; if (_pb) _pb.disabled = \2; }",
        content
    )
    content = re.sub(
        r"(\$\('next-btn'\)|document\.getElementById\('next-btn'\))\.disabled\s*=\s*([^;]+);",
        r"{ const _nb = \1; if (_nb) _nb.disabled = \2; }",
        content
    )
    content = re.sub(
        r"(\$\('btn-prev'\)|document\.getElementById\('btn-prev'\))\.disabled\s*=\s*([^;]+);",
        r"{ const _bp = \1; if (_bp) _bp.disabled = \2; }",
        content
    )
    content = re.sub(
        r"(\$\('btn-next'\)|document\.getElementById\('btn-next'\))\.disabled\s*=\s*([^;]+);",
        r"{ const _bn = \1; if (_bn) _bn.disabled = \2; }",
        content
    )

    # 2. Where we have: const nextBtn = document.getElementById('next-btn');
    # followed by uses of nextBtn.xxx, wrap the whole block
    # Pattern: variable declaration + subsequent uses in same block
    # This is complex - instead, add optional chaining where possible

    # Replace: nextBtn.xxx → nextBtn?.xxx (optional chaining)
    # But only in JS context. We'll do targeted replacements.

    # Replace shorthand references like:
    # const prevBtn=$('prev-btn'), nextBtn=$('next-btn');
    # prevBtn.disabled = ...; nextBtn.xxx = ...;
    # → Make them null-safe
    content = re.sub(
        r"const prevBtn\s*=\s*\$\('prev-btn'\)\s*,\s*nextBtn\s*=\s*\$\('next-btn'\);",
        "const prevBtn = document.getElementById('prev-btn'), nextBtn = document.getElementById('next-btn');",
        content
    )

    # For patterns like:
    # const nextBtn = $('next-btn');
    # nextBtn.innerHTML = '...';
    # nextBtn.onclick = ...;
    # → const nextBtn = document.getElementById('next-btn'); if (nextBtn) { ... }
    # This is too complex to do generically. Instead, use optional chaining on properties.

    # Replace .textContent, .innerHTML, .style, .onclick, .disabled on these vars
    # with optional chaining using ?. operator

    # For the pattern where we assign to prevBtn/nextBtn from getElementById
    # and then use them, make the usage optional-chaining

    # Simple targeted patterns for common button variables
    for btn_var in ['nextBtn', 'prevBtn', 'btnPrev', 'btnNext', 'btn_prev', 'btn_next']:
        # nextBtn.disabled = ... → if (nextBtn) nextBtn.disabled = ...
        content = re.sub(
            rf'\b{re.escape(btn_var)}\.(disabled|textContent|innerHTML|style\.\w+|onclick)\s*=\s*([^;]+);',
            rf'if ({btn_var}) {btn_var}.\1 = \2;',
            content
        )
        # nextBtn.style.visibility = ... → if (nextBtn) nextBtn.style.visibility = ...
        content = re.sub(
            rf'\b{re.escape(btn_var)}\.style\.(\w+)\s*=\s*([^;]+);',
            rf'if ({btn_var}) {btn_var}.style.\1 = \2;',
            content
        )

    # Also handle direct chained property access from getElementById
    # document.getElementById('next-btn').textContent = ... → null-safe
    content = re.sub(
        r"document\.getElementById\('next-btn'\)\.(\w+)\s*=\s*([^;]+);",
        r"{ const _nb = document.getElementById('next-btn'); if (_nb) _nb.\1 = \2; }",
        content
    )
    content = re.sub(
        r"document\.getElementById\('prev-btn'\)\.(\w+)\s*=\s*([^;]+);",
        r"{ const _pb = document.getElementById('prev-btn'); if (_pb) _pb.\1 = \2; }",
        content
    )

    # Handle $('prev-btn') and $('next-btn') (shorthand used in some modules)
    # Replace: $('prev-btn').disabled = ... → { const _pb = $('prev-btn'); if (_pb) _pb.disabled = ...; }
    content = re.sub(
        r"\$\('prev-btn'\)\.(\w+)\s*=\s*([^;]+);",
        r"{ const _pb = $('prev-btn'); if (_pb) _pb.\1 = \2; }",
        content
    )
    content = re.sub(
        r"\$\('next-btn'\)\.(\w+)\s*=\s*([^;]+);",
        r"{ const _nb = $('next-btn'); if (_nb) _nb.\1 = \2; }",
        content
    )

    return content


def process_file(filename):
    filepath = os.path.join(BASE, filename)
    print(f"Processing {filename} ...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = fix_btn_references(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed JS button references")
    else:
        print(f"  - No changes needed")

    return content != original


if __name__ == '__main__':
    changed = 0
    for f in FILES:
        if process_file(f):
            changed += 1
    print(f"\nDone. {changed}/{len(FILES)} files updated.")
