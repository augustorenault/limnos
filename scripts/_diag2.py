import glob

for path in sorted(glob.glob("src/pages/servicos/*/index.astro")):
    lines = open(path, encoding="utf-8").read().split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith('const content = "')), None)
    end = start
    while end < len(lines) and not lines[end].rstrip().endswith('";'):
        end += 1
    slug = path.replace("\\", "/").split("/servicos/")[1].split("/")[0]
    cards = open(path, encoding="utf-8").read().count("card-dr-pattern")
    print(f"{slug}: content span={end-start+1}, card-dr-pattern={cards}")
