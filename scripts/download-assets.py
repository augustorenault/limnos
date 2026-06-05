"""Baixa do site oficial todas as imagens/videos referenciados localmente.

Varre o HTML gerado em dist/ e o CSS em public/css, coleta os caminhos de
assets (mesma origem, raiz-relativos) e baixa cada arquivo para public/,
preservando a estrutura de pastas. Ignora o que ja existe e o que e externo
(CDNs). Usa User-Agent de navegador (o Nginx do site bloqueia agentes padrao).
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import stat as statmod
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC = ROOT / "public"
CSS = PUBLIC / "css" / "limnos-site.css"

BASE = "https://www.limnos.com.br"
DOMAIN = "www.limnos.com.br"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

EXTS = (
    ".webp", ".jpg", ".jpeg", ".png", ".gif", ".svg",
    ".ico", ".avif", ".mp4", ".webm",
)

ATTR_RE = re.compile(r'(?:src|href|poster|data-lazy)\s*=\s*"([^"]+)"', re.I)
CSS_URL_RE = re.compile(r'url\(\s*[\'"]?([^)\'"]+)[\'"]?\s*\)', re.I)


def to_path(url: str):
    """Converte uma referencia em caminho raiz-relativo (ou None se externa)."""
    url = url.split("#", 1)[0].split("?", 1)[0].strip()
    if not url:
        return None
    if url.startswith(BASE):
        url = url[len(BASE):]
    elif url.startswith("//" + DOMAIN):
        url = url[len("//" + DOMAIN):]
    elif url.startswith("http://") or url.startswith("https://") or url.startswith("//"):
        return None  # outra origem (CDN)
    if not url.startswith("/"):
        return None
    if not url.lower().endswith(EXTS):
        return None
    return url


def collect():
    paths = set()
    for html in DIST.rglob("*.html"):
        text = html.read_text(encoding="utf-8", errors="replace")
        for m in ATTR_RE.finditer(text):
            p = to_path(m.group(1))
            if p:
                paths.add(p)
    if CSS.exists():
        text = CSS.read_text(encoding="utf-8", errors="replace")
        for m in CSS_URL_RE.finditer(text):
            p = to_path(m.group(1))
            if p:
                paths.add(p)
    return sorted(paths)


def is_cloud_placeholder(p: Path) -> bool:
    """Detecta arquivo 'somente na nuvem' do OneDrive (reparse/recall)."""
    try:
        attrs = p.stat().st_file_attributes
    except (AttributeError, OSError):
        return False
    reparse = getattr(statmod, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    recall_open = 0x00040000  # FILE_ATTRIBUTE_RECALL_ON_OPEN
    recall_access = 0x00400000  # FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS
    return bool(attrs & (reparse | recall_open | recall_access))


def download(path: str):
    dest = PUBLIC / path.lstrip("/")
    # Pula apenas se for arquivo real e local (nao placeholder de nuvem).
    if dest.exists() and dest.stat().st_size > 0 and not is_cloud_placeholder(dest):
        return ("skip", path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        if not data:
            return ("empty", path)
        dest.write_bytes(data)
        return ("ok", path)
    except urllib.error.HTTPError as e:
        return ("http %s" % e.code, path)
    except Exception as e:  # noqa: BLE001
        return ("err %s" % type(e).__name__, path)


def main():
    paths = collect()
    print(f"Referencias de assets encontradas: {len(paths)}")

    results = {}
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(download, p): p for p in paths}
        for fut in as_completed(futures):
            status, path = fut.result()
            results.setdefault(status, []).append(path)

    ok = len(results.get("ok", []))
    skip = len(results.get("skip", []))
    print(f"\nBaixados: {ok} | Ja existiam: {skip}")

    fails = {k: v for k, v in results.items() if k not in ("ok", "skip")}
    if fails:
        total = sum(len(v) for v in fails.values())
        print(f"\nFalhas: {total}")
        for status, items in sorted(fails.items()):
            print(f"  [{status}] {len(items)}")
            for it in items[:15]:
                print(f"      {it}")
            if len(items) > 15:
                print(f"      ... +{len(items) - 15}")


if __name__ == "__main__":
    main()
