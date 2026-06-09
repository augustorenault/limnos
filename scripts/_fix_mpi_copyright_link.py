import glob

OLD = "entre em contato conosco."
NEW = (
    '<a href=\\"/contato\\" title=\\"Entre em contato\\">entre em contato conosco</a>.'
)

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

    if OLD not in text or NEW in text:
        continue

    text = text.replace(OLD, NEW, 1)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    updated += 1

print(f"updated: {updated}")
