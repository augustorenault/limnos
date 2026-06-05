"""Extrai o conteúdo principal da homepage para o Astro."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT.parent / "01-backup-original" / "www.limnos.com.br" / "index.html"
OUT = ROOT / "src" / "components" / "HomeMainContent.astro"

lines = BACKUP.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)

# barra_doutor (6143-6144) + conteúdo interno do <main> (6145-6342)
raw = "".join(lines[6142:6343])

# Remove tags <main> se presentes
raw = re.sub(r"</?main>", "", raw, flags=re.I)

def fix_paths(s: str) -> str:
    s = s.replace("https://www.limnos.com.br/", "/")
    s = s.replace("https://www.limnos.com.br", "/")
    return s

content = fix_paths(raw.strip())

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("---\n---\n" + content + "\n", encoding="utf-8")
print(f"Written {OUT} ({len(content)} chars)")
