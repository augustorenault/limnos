import glob
import re


def merge_content_string(text: str) -> str:
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith('const content = "')), None)
    if start is None:
        return text
    end = start
    while end < len(lines) and not lines[end].rstrip().endswith('";'):
        end += 1
    if end >= len(lines):
        return text

    prefix = lines[start][: len('const content = "')]
    chunks = []
    for i in range(start, end + 1):
        chunk = lines[i]
        if i == start:
            chunk = chunk[len('const content = "'):]
        if i == end:
            chunk = chunk[: -len('";')]
        chunks.append(chunk)
    inner = "\\n".join(chunks)
    new_line = f'{prefix}{inner}";'
    return "\n".join(lines[:start] + [new_line] + lines[end + 1 :])


ASIDE_CONTATO = re.compile(
    r'<div class=\\"aside__contato\\">[\s\S]*?</div>\\n(?=</aside>)',
)


skip = {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}
updated = 0
skipped = 0

for path in sorted(glob.glob("src/pages/**/index.astro", recursive=True)):
    norm = path.replace("\\", "/")
    if "/servicos/" in norm:
        continue
    slug = norm.split("/pages/")[1].replace("/index.astro", "")
    if slug in skip:
        continue

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if 'const content = "' not in text or "aside__contato" not in text:
        skipped += 1
        continue

    text = merge_content_string(text)
    start = text.index('const content = "') + len('const content = "')
    end = text.rindex('";')
    content = text[start:end]

    new_content, count = ASIDE_CONTATO.subn("", content, count=1)
    if count != 1:
        skipped += 1
        continue

    new_text = text[:start] + new_content + text[end:]
    new_text = merge_content_string(new_text)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    updated += 1

print(f"updated: {updated}, skipped: {skipped}")
