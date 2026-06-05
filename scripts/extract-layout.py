"""Extrai CSS, header e footer do backup."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT.parent / "01-backup-original" / "www.limnos.com.br" / "index.html"
lines = BACKUP.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)


def fix_paths(s: str) -> str:
    s = s.replace("https://www.limnos.com.br/", "/")
    s = s.replace("https://www.limnos.com.br", "/")
    return re.sub(r'\s*<base\s+href="[^"]*"\s*/?>\s*', "\n", s, flags=re.I)


# CSS: linhas 59-5691 (bloco principal no head)
css = "".join(lines[58:5691])
if "<style>" in css:
    css = css.split("<style>", 1)[1]
if "</style>" in css:
    css = css.rsplit("</style>", 1)[0]
(ROOT / "public" / "css" / "limnos-site.css").parent.mkdir(parents=True, exist_ok=True)
(ROOT / "public" / "css" / "limnos-site.css").write_text(css.strip() + "\n", encoding="utf-8")

# Header linhas 5698-6140, footer 6345-6469
header = fix_paths("".join(lines[5697:6140]))
footer = fix_paths("".join(lines[6344:6469]))

(ROOT / "src" / "components").mkdir(parents=True, exist_ok=True)
(ROOT / "src" / "components" / "SiteHeader.astro").write_text(
    "---\n---\n" + header, encoding="utf-8"
)
(ROOT / "src" / "components" / "SiteFooter.astro").write_text(
    "---\n---\n" + footer, encoding="utf-8"
)
print("OK", len(header), len(footer))
print(header[:120].replace("\n", " "))
