"""Migracao em lote das paginas clonadas (backup HTML) para paginas .astro.

Para cada pagina HTML do backup (exceto a home e o contato, ja migrados):
- extrai <title>, description e keywords;
- extrai o conteudo interno de <main>...</main>;
- corrige caminhos absolutos para a raiz local (/...);
- limpa links internos terminados em .html -> rota limpa;
- gera src/pages/<mesma-estrutura>/index.astro usando o Layout mestre.

O HTML e injetado via <Fragment set:html={content} /> com strings em JSON,
garantindo build limpo independente do conteudo clonado.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from strip_regions import strip_regions_section  # noqa: E402
BACKUP = ROOT.parent / "01-backup-original" / "www.limnos.com.br"
PAGES = ROOT / "src" / "pages"

# Paginas que NAO devem ser migradas (ja existem / fora de escopo).
SKIP_DIRS = {"contato"}


def fix_paths(s: str) -> str:
    s = s.replace("https://www.limnos.com.br/", "/")
    s = s.replace("https://www.limnos.com.br", "/")
    s = re.sub(r'\s*<base\s+href="[^"]*"\s*/?>\s*', "", s, flags=re.I)
    return s


def clean_internal_links(s: str) -> str:
    """href="/algo/index.html" -> "/algo"; href="/algo.html" -> "/algo"."""
    s = re.sub(r'(href=")(/[^"]*?)/index\.html(")', r"\1\2\3", s, flags=re.I)
    s = re.sub(r'(href=")(/[^"]*?)\.html(")', r"\1\2\3", s, flags=re.I)
    return s


def meta(pattern: str, html: str) -> str:
    m = re.search(pattern, html, flags=re.I | re.S)
    return m.group(1).strip() if m else ""


def extract_main(html: str) -> str:
    m = re.search(r"<main[^>]*>(.*?)</main>", html, flags=re.I | re.S)
    return m.group(1).strip() if m else ""


def rel_layout_import(out_file: Path) -> str:
    """Caminho relativo da pagina ate src/layouts/Layout.astro."""
    layout = ROOT / "src" / "layouts" / "Layout.astro"
    rel = Path(__file__)  # placeholder
    import os

    rel = os.path.relpath(layout, out_file.parent)
    return rel.replace("\\", "/")


written, skipped = [], []

for src in sorted(BACKUP.rglob("index.html")):
    rel = src.relative_to(BACKUP)
    rel_dir = rel.parent  # "" para a home

    # Pula home e diretorios fora de escopo.
    if str(rel_dir) in (".", ""):
        skipped.append((str(rel), "home"))
        continue
    if rel_dir.parts[0] in SKIP_DIRS:
        skipped.append((str(rel), "fora de escopo"))
        continue

    html = src.read_text(encoding="utf-8", errors="replace")

    title = meta(r"<title>(.*?)</title>", html)
    description = meta(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    keywords = meta(r'<meta\s+name="keywords"\s+content="([^"]*)"', html)

    if not title:
        skipped.append((str(rel), "sem title (artefato)"))
        continue

    content = extract_main(html)
    if not content:
        skipped.append((str(rel), "sem <main>"))
        continue

    content = strip_regions_section(clean_internal_links(fix_paths(content)))

    out_file = PAGES / rel_dir / "index.astro"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    layout_import = rel_layout_import(out_file)

    astro = (
        "---\n"
        f"import Layout from '{layout_import}';\n\n"
        f"const title = {json.dumps(title, ensure_ascii=False)};\n"
        f"const description = {json.dumps(description, ensure_ascii=False)};\n"
        f"const keywords = {json.dumps(keywords, ensure_ascii=False)};\n"
        f"const content = {json.dumps(content, ensure_ascii=False)};\n"
        "---\n\n"
        "<Layout title={title} description={description} keywords={keywords}>\n"
        "  <Fragment set:html={content} />\n"
        "</Layout>\n"
    )

    out_file.write_text(astro, encoding="utf-8")
    written.append(str(rel_dir).replace("\\", "/"))

print(f"Paginas geradas: {len(written)}")
for w in written:
    print("  +", w)
print(f"\nIgnoradas: {len(skipped)}")
for s, why in skipped:
    print(f"  - {s}  ({why})")
