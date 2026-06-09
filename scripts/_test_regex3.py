import re

# merge only - no import of fix module
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

print("merged real NL count", merged.count("\n"), "lines", len(merged.split("\n")))

# inline related block minimal test - just replace with SHORT marker
PATTERN = re.compile(
    r'<div class=\\"container\\">\\n\s*<div class=\\"serv-inc__related\\">.*?</div>\s*\\n\s*</div>\s*\\n<script>',
    re.DOTALL,
)
m = PATTERN.search(merged)
if m:
    print("match len", len(m.group(0)))
    print("match start", m.start(), "end", m.end())
    print("match preview start", repr(m.group(0)[:120]))
    print("match preview end", repr(m.group(0)[-120:]))
else:
    print("NO MATCH")

updated, count = PATTERN.subn("REPLACED_MARKER<script>", merged, count=1)
print("after sub lines", len(updated.split("\n")), "real NL", updated.count("\n"))
