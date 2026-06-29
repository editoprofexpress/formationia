#!/usr/bin/env python3
"""
Supprime tous les commentaires HTML/CSS/JS des modules.
- HTML  : <!-- ... -->
- CSS   : /* ... */
- JS    : // ...  et /* ... */
Respecte les strings (', ", `) et les URLs https://
"""
import re, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── Strip commentaires JS ────────────────────────────────────────────────────

def strip_js_comments(code: str) -> str:
    result = []
    i = 0
    n = len(code)

    while i < n:
        c = code[i]

        # ── String simple quote ────────────────────────────────────────────
        if c == "'":
            j = i + 1
            while j < n:
                if code[j] == '\\': j += 2; continue
                if code[j] == "'":  j += 1; break
                j += 1
            result.append(code[i:j]); i = j

        # ── String double quote ───────────────────────────────────────────
        elif c == '"':
            j = i + 1
            while j < n:
                if code[j] == '\\': j += 2; continue
                if code[j] == '"':  j += 1; break
                j += 1
            result.append(code[i:j]); i = j

        # ── Template literal (backtick) ──────────────────────────────────
        # On copie tout jusqu'au backtick fermant sans modifier le contenu
        elif c == '`':
            j = i + 1
            depth = 0
            while j < n:
                if code[j] == '\\':
                    j += 2; continue
                if code[j] == '$' and j + 1 < n and code[j+1] == '{':
                    depth += 1; j += 2; continue
                if code[j] == '}' and depth > 0:
                    depth -= 1; j += 1; continue
                if code[j] == '`' and depth == 0:
                    j += 1; break
                j += 1
            result.append(code[i:j]); i = j

        # ── Commentaire bloc /* ... */ ────────────────────────────────────
        elif c == '/' and i + 1 < n and code[i+1] == '*':
            end = code.find('*/', i + 2)
            if end == -1:
                i = n
            else:
                # Préserver le nombre de sauts de ligne
                skipped = code[i:end+2]
                result.append('\n' * skipped.count('\n'))
                i = end + 2

        # ── Commentaire ligne // ──────────────────────────────────────────
        elif c == '/' and i + 1 < n and code[i+1] == '/':
            end = code.find('\n', i + 2)
            if end == -1:
                i = n
            else:
                # Ne PAS émettre de \n ici — le \n naturel à 'end' sera
                # traité dans le prochain tour (i = end, pas end+1)
                i = end  # le '\n' en [end] sera émis normalement

        else:
            result.append(c)
            i += 1

    return ''.join(result)

# ─── Strip commentaires CSS ───────────────────────────────────────────────────

def strip_css_comments(css: str) -> str:
    result = []
    i = 0
    n = len(css)
    while i < n:
        if css[i] == '/' and i + 1 < n and css[i+1] == '*':
            end = css.find('*/', i + 2)
            if end == -1:
                i = n
            else:
                skipped = css[i:end+2]
                result.append('\n' * skipped.count('\n'))
                i = end + 2
        else:
            result.append(css[i])
            i += 1
    return ''.join(result)

# ─── Traitement HTML ─────────────────────────────────────────────────────────

def process_html(content: str) -> str:
    out = []
    i = 0
    n = len(content)

    while i < n:
        # ── Commentaire HTML <!-- ... --> ─────────────────────────────────
        if content[i:i+4] == '<!--':
            end = content.find('-->', i + 4)
            if end == -1:
                out.append(content[i]); i += 1
            else:
                skipped = content[i:end+3]
                out.append('\n' * skipped.count('\n'))
                i = end + 3

        # ── Bloc <style> ─────────────────────────────────────────────────
        elif content[i:i+6].lower() == '<style':
            tag_end = content.find('>', i + 6)
            if tag_end == -1:
                out.append(content[i]); i += 1; continue
            opening_tag = content[i:tag_end+1]
            close = re.search(r'</style\s*>', content[tag_end+1:], re.IGNORECASE)
            if close is None:
                out.append(content[i]); i += 1; continue
            css_start = tag_end + 1
            css_end   = tag_end + 1 + close.start()
            css_close = content[css_end:css_end + close.end() - close.start()]
            clean_css = strip_css_comments(content[css_start:css_end])
            out.append(opening_tag + clean_css + css_close)
            i = css_end + len(css_close)

        # ── Bloc <script> ────────────────────────────────────────────────
        elif content[i:i+7].lower() == '<script':
            tag_end = content.find('>', i + 7)
            if tag_end == -1:
                out.append(content[i]); i += 1; continue
            opening_tag = content[i:tag_end+1]
            close = re.search(r'</script\s*>', content[tag_end+1:], re.IGNORECASE)
            if close is None:
                out.append(content[i]); i += 1; continue
            js_start = tag_end + 1
            js_end   = tag_end + 1 + close.start()
            js_close = content[js_end:js_end + close.end() - close.start()]
            clean_js = strip_js_comments(content[js_start:js_end])
            out.append(opening_tag + clean_js + js_close)
            i = js_end + len(js_close)

        else:
            out.append(content[i])
            i += 1

    return ''.join(out)

# ─── Nettoyage lignes vides ───────────────────────────────────────────────────

def normalize_blank_lines(content: str) -> str:
    # Convertir les lignes contenant uniquement des espaces en vraies lignes vides
    content = re.sub(r'\n[ \t]+\n', '\n\n', content)
    # Supprimer les lignes avec seulement des espaces en début/fin de bloc CSS
    # Limiter à 2 lignes vides consécutives max
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

# ─── Lancement ───────────────────────────────────────────────────────────────

files = sorted(glob.glob(os.path.join(BASE, 'module*.html')))
print(f"Suppression des commentaires dans {len(files)} fichiers...\n")

for path in files:
    fname = os.path.basename(path)
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    processed = process_html(original)
    # Second passage : supprimer les <!-- --> restants (dans les template literals JS)
    processed = re.sub(r'<!--.*?-->', '', processed, flags=re.DOTALL)
    processed = normalize_blank_lines(processed)

    orig_lines = original.count('\n')
    proc_lines = processed.count('\n')
    diff = orig_lines - proc_lines

    with open(path, 'w', encoding='utf-8') as f:
        f.write(processed)

    sign = '-' if diff >= 0 else '+'
    print(f'✅ {fname}: {orig_lines} → {proc_lines} lignes ({sign}{abs(diff)})')

print("\n✅ Terminé.")
