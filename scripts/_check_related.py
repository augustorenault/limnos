import glob
import re

for path in sorted(glob.glob("src/pages/servicos/*/index.astro")):
    t = open(path, encoding="utf-8").read()
    idx = t.find("serv-inc__related")
    if idx < 0:
        continue
    end = t.find("<script>", idx)
    block = t[idx:end if end > idx else idx + 12000]
    cards = len(re.findall(r'card-dr-pattern', block))
    links = list(dict.fromkeys(re.findall(r'href=\\"(/servicos/[^\\"]+)\\"', block)))
    slug = path.replace("\\", "/").split("/servicos/")[1].split("/")[0]
    print(f"{slug}: {cards} cards, {len(links)} unique links")
    for l in links:
        print(f"  - {l}")
