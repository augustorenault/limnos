path = "src/pages/servicos/monitoramento-de-qualidade-do-ar/index.astro"
text = open(path, encoding="utf-8").read()
lines = text.split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith('const content = "'))
end = start
while end < len(lines) and not lines[end].rstrip().endswith('";'):
    end += 1
prefix = lines[start][: len('const content = "')]
chunks = []
for i in range(start, end + 1):
    chunk = lines[i]
    if i == start:
        chunk = chunk[len('const content = "'):]
    if i == end:
        chunk = chunk[: -len('";')]
    chunks.append(chunk)
inner = "\\n".join(chunks)
new_line = f'{prefix}{inner}";'
merged = "\n".join(lines[:start] + [new_line] + lines[end + 1 :])
print("before", len(lines), "after", len(merged.split("\n")))
out = "scripts/_test_merged.astro"
open(out, "w", encoding="utf-8", newline="").write(merged)
print("written", out, "lines", len(open(out, encoding="utf-8").read().split("\n")))
