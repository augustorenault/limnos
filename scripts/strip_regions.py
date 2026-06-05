"""Remove a secao 'Regioes onde a Limnos atende...' das paginas .astro migradas."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"

REGIONS_HEAD = re.compile(
    r'(?:<div class="clear"></div>\s*)?'
    r'<h2 class="text-center">Regiões onde a Limnos atende[^<]*</h2><br>\s*'
    r'<div class="organictabs--regioes">',
    re.I | re.S,
)
TRAILING_CLEAR = re.compile(r'^\s*<div class="clear"></div>', re.I)


def _close_div_at(html: str, pos: int) -> int:
    depth = 0
    i = pos
    n = len(html)
    while i < n:
        if i + 4 <= n and html[i : i + 4].lower() == "<div":
            nxt = html[i + 4] if i + 4 < n else ""
            if nxt in (" ", ">", "\t", "\n", "/"):
                depth += 1
                i += 4
                continue
        if i + 6 <= n and html[i : i + 6].lower() == "</div>":
            depth -= 1
            i += 6
            if depth == 0:
                return i
            continue
        i += 1
    return n


def strip_regions_section(html: str) -> str:
    m = REGIONS_HEAD.search(html)
    if not m:
        return html

    start = m.start()
    ot = html.find('<div class="organictabs--regioes">', m.start(), m.end() + 40)
    if ot < 0:
        return html

    end = _close_div_at(html, ot)
    rest = html[end:]
    clear_m = TRAILING_CLEAR.match(rest)
    if clear_m:
        end += clear_m.end()

    return html[:start] + html[end:]


def update_astro(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "organictabs--regioes" not in text:
        return False

    m = re.search(r"const content = (.+);\s*\n---", text, re.S)
    if not m:
        print(f"  ! sem const content: {path.relative_to(ROOT)}")
        return False

    content = json.loads(m.group(1))
    new_content = strip_regions_section(content)
    if new_content == content:
        return False

    new_text = text[: m.start(1)] + json.dumps(new_content, ensure_ascii=False) + text[m.end(1) :]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    updated = []
    for astro in sorted(PAGES.rglob("index.astro")):
        if update_astro(astro):
            updated.append(astro.relative_to(ROOT))

    print(f"Paginas atualizadas: {len(updated)}")
    for p in updated:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
