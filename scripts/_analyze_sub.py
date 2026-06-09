import re

code = open("scripts/_fix_all_services.py", encoding="utf-8").read().split("RELATED_PATTERN")[0]
ns = {}
exec(code, ns)
related_block = ns["related_block"]

merged = open("scripts/_test_merged.astro", encoding="utf-8").read()
slug = "monitoramento-de-qualidade-do-ar"
new_block = related_block(slug)
replacement = '<div class=\\"container\\">\\n        ' + new_block + '\\n    </div>\\n<script>'
print("replacement chars 20-35", [ord(c) for c in replacement[20:35]])
print("replacement repr 0-80", repr(replacement[:80]))
PATTERN = re.compile(
    r'<div class=\\"container\\">\\n\s*<div class=\\"serv-inc__related\\">.*?</div>\s*\\n\s*</div>\s*\\n<script>',
    re.DOTALL,
)
m = PATTERN.search(merged)
updated, _ = PATTERN.subn(replacement, merged, count=1)

print("match start", m.start(), "end", m.end(), "repl len", len(replacement))
print("merged len", len(merged), "updated len", len(updated))
print("updated real NL count", updated.count("\n"))
print("char at 8788-8792", repr(updated[8785:8795]))

# compare: expected single line content
lines = merged.split("\n")
content_line = lines[6]
print("content line len before", len(content_line))

# where does match start relative to content line?
# find content line start in merged
idx = merged.index('const content = "')
print("content starts at file pos", idx)
print("match start relative to content", m.start() - idx)

# after sub, find first real newline after const content = "
start = updated.index('const content = "')
for i in range(start, len(updated)):
    if updated[i] == "\n":
        print("first NL after content start at file pos", i, "offset in content", i - start)
        print("context before NL", repr(updated[i - 50 : i]))
        print("context after NL", repr(updated[i : i + 50]))
        break
