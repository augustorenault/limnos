import glob

OLD = '</aside>\\n        </div>\\n    <div class=\\"bg-cta-pattern'
NEW = '</aside>\\n        </div>\\n    </div>\\n</div>\\n<div class=\\"bg-cta-pattern'

for path in sorted(glob.glob("src/pages/servicos/*/index.astro")):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if OLD not in text:
        print(f"skip (pattern not found): {path}")
        continue
    text = text.replace(OLD, NEW, 1)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"fixed: {path}")

print("done")
