import glob

OLD = '</aside>\\n<div class=\\"bg-cta-pattern cta-video'
NEW = '</aside>\\n<br class=\\"clear\\">\\n<div class=\\"bg-cta-pattern cta-video'

skip = {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}
updated = 0

for path in sorted(glob.glob("src/pages/**/index.astro", recursive=True)):
    norm = path.replace("\\", "/")
    if "/servicos/" in norm:
        continue
    slug = norm.split("/pages/")[1].replace("/index.astro", "")
    if slug in skip:
        continue

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if OLD not in text:
        continue

    text = text.replace(OLD, NEW, 1)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    updated += 1

print(f"updated: {updated}")
