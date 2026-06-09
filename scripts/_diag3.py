import glob

path = "src/pages/servicos/monitoramento-de-emissoes-atmosfericas/index.astro"
lines = open(path, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith('const content = "'))
end = start
while end < len(lines) and not lines[end].rstrip().endswith('";'):
    end += 1
print("start", start, "end", end, "total", len(lines))
print("span", end - start + 1)
print("line start len", len(lines[start]))
print("line end preview", lines[end][:80], "...")
print("line end suffix", repr(lines[end][-20:]))

# test merge
import importlib.util
spec = importlib.util.spec_from_file_location("repair", "scripts/_repair_and_related.py")
repair = importlib.util.module_from_spec(spec)
# just run merge function inline
text = open(path, encoding="utf-8").read()

def merge_content_string(text: str) -> str:
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith('const content = "')), None)
    if start is None:
        return text
    end = start
    while end < len(lines) and not lines[end].rstrip().endswith('";'):
        end += 1
    if end >= len(lines):
        return text
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
    return "\n".join(lines[:start] + [new_line] + lines[end + 1 :])

merged = merge_content_string(text)
mlines = merged.split("\n")
mstart = next(i for i, l in enumerate(mlines) if l.startswith('const content = "'))
mend = mstart
while mend < len(mlines) and not mlines[mend].rstrip().endswith('";'):
    mend += 1
print("after merge span", mend - mstart + 1, "total lines", len(mlines))
