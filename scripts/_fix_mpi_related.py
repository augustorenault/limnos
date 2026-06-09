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


def load_page_meta() -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}
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
        meta[f"/{slug}"] = {"description": desc}
    return meta


WS = r"(?:\\n| )*"

CARD_PATTERN = re.compile(
    rf'<div class=\\"card--mod-23\\">{WS}'
    rf'<img class=\\"card__image\\" src=\\"([^\\"]+)\\"[^>]*>{WS}'
    rf'<div class=\\"card__description\\">{WS}'
    rf'<h3 class=\\"card__title\\">([^<]*)</h3>.*?'
    rf'<a class=\\"card__link\\" rel=\\"nofollow\\" href=\\"([^\\"]+)\\"',
    re.DOTALL,
)

RELATED_PATTERN = re.compile(
    r'<div class=\\"related-posting\\">[\s\S]*?(?=\\n\s*<br class=\\"clear\\">)'
)


def html_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def build_card(href: str, title: str, image: str, description: str) -> str:
    title_e = html_escape(title)
    href_e = html_escape(href)
    image_e = html_escape(image)
    desc_e = html_escape(description)
    return (
        '                                    <div class=\\"col-12 col-md-6 col-lg-3 pb-4 card-dr-pattern\\">\\n'
        f'                        <a class=\\"card card--related-serv\\" href=\\"{href_e}\\" title=\\"{title_e}\\">\\n'
        '                            <div class=\\"card--related-serv__media\\">\\n'
        f'                                <img loading=\\"lazy\\" src=\\"{image_e}\\" alt=\\"{title_e}\\" title=\\"{title_e}\\">\\n'
        '                            </div>\\n'
        '                            <div class=\\"card-body\\">\\n'
        f'                                <h2 class=\\"card-title\\">{title_e}</h2>\\n'
        f'                                <p class=\\"card__description\\">{desc_e}</p>\\n'
        '                                <span class=\\"btn-link btn-link--primary\\">Saiba Mais</span>\\n'
        '                            </div>\\n'
        '                        </a>\\n'
        '                    </div>'
    )


def build_related_section(cards_html: str) -> str:
    return (
        '<div class=\\"container\\">\\n'
        '    <div class=\\"serv-inc__related\\">\\n'
        '        <h2 class=\\"title-subtitle text-center fs-2 my-5\\"><span>Confira Também</span>Páginas relacionadas</h2>\\n'
        '        <div class=\\"row justify-content-center align-items-start\\">\\n'
        f'{cards_html}\\n'
        '        </div>\\n'
        '    </div>\\n'
        '</div>'
    )


def transform_content(content: str, meta: dict[str, dict[str, str]]) -> tuple[str, bool]:
    if "card--mod-23" not in content and "serv-inc__related" in content:
        return content, False
    if "related-posting" not in content:
        return content, False

    cards = CARD_PATTERN.findall(content)
    if not cards:
        return content, False

    card_html = []
    for image, title, href in cards:
        description = meta.get(href, {}).get("description", f"Saiba mais sobre {title}.")
        card_html.append(build_card(href, title.strip(), image, description))

    new_section = build_related_section("".join(card_html))

    def repl(_m: re.Match) -> str:
        return new_section

    updated, count = RELATED_PATTERN.subn(repl, content, count=1)
    return updated, count == 1


meta = load_page_meta()
updated_count = 0
skipped = 0

for path in sorted(glob.glob("src/pages/**/index.astro", recursive=True)):
    norm = path.replace("\\", "/")
    if "/servicos/" in norm:
        continue
    slug = norm.split("/pages/")[1].replace("/index.astro", "")
    if slug in {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}:
        continue

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if 'const content = "' not in text:
        continue

    text = merge_content_string(text)
    start = text.index('const content = "') + len('const content = "')
    end = text.rindex('";')
    content = text[start:end]

    new_content, ok = transform_content(content, meta)
    if not ok:
        skipped += 1
        continue

    new_text = text[:start] + new_content + text[end:]
    new_text = merge_content_string(new_text)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    updated_count += 1

print(f"updated: {updated_count}, skipped: {skipped}, meta pages: {len(meta)}")
