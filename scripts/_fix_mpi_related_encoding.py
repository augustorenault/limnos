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


def decode_js_string(value: str) -> str:
    """Desfaz escapes JS sem corromper caracteres UTF-8."""
    out = []
    i = 0
    while i < len(value):
        ch = value[i]
        if ch == "\\" and i + 1 < len(value):
            nxt = value[i + 1]
            if nxt == "n":
                out.append("\n")
                i += 2
                continue
            if nxt == "r":
                out.append("\r")
                i += 2
                continue
            if nxt == "t":
                out.append("\t")
                i += 2
                continue
            if nxt == '"':
                out.append('"')
                i += 2
                continue
            if nxt == "\\":
                out.append("\\")
                i += 2
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def html_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def load_page_meta() -> dict[str, str]:
    meta: dict[str, str] = {}
    skip = {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}
    for path in glob.glob("src/pages/**/index.astro", recursive=True):
        norm = path.replace("\\", "/")
        if "/servicos/" in norm:
            continue
        slug = norm.split("/pages/")[1].replace("/index.astro", "")
        if slug in skip:
            continue
        text = open(path, encoding="utf-8").read()
        m_desc = re.search(r'const description = "(.*?)";\n', text, re.DOTALL)
        if not m_desc:
            continue
        desc = decode_js_string(m_desc.group(1))
        if len(desc) > 220:
            desc = desc[:217].rsplit(" ", 1)[0] + "..."
        meta[f"/{slug}"] = desc
    return meta


CARD_DESC_PATTERN = re.compile(
    r'(<a class=\\"card card--related-serv\\" href=\\"([^\\"]+)\\"[^>]*>.*?'
    r'<p class=\\"card__description\\">)([^<]*)(</p>)',
    re.DOTALL,
)


def fix_descriptions(content: str, meta: dict[str, str]) -> tuple[str, int]:
    fixes = 0

    def repl(m: re.Match) -> str:
        nonlocal fixes
        prefix, href, _old, suffix = m.group(1), m.group(2), m.group(3), m.group(4)
        if href not in meta:
            return m.group(0)
        fixes += 1
        return f"{prefix}{html_escape(meta[href])}{suffix}"

    new_content = CARD_DESC_PATTERN.sub(repl, content)
    return new_content, fixes


meta = load_page_meta()
total_pages = 0
total_fixes = 0

for path in sorted(glob.glob("src/pages/**/index.astro", recursive=True)):
    norm = path.replace("\\", "/")
    if "/servicos/" in norm:
        continue
    slug = norm.split("/pages/")[1].replace("/index.astro", "")
    if slug in {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}:
        continue

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if "card--related-serv" not in text:
        continue

    text = merge_content_string(text)
    start = text.index('const content = "') + len('const content = "')
    end = text.rindex('";')
    content = text[start:end]

    new_content, fixes = fix_descriptions(content, meta)
    if fixes == 0:
        continue

    new_text = text[:start] + new_content + text[end:]
    new_text = merge_content_string(new_text)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)

    total_pages += 1
    total_fixes += fixes

print(f"pages fixed: {total_pages}, descriptions fixed: {total_fixes}")
