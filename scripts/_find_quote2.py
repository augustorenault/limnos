import re
import importlib.util

# copy related_block from fix without running main
path_merged = "scripts/_test_merged.astro"
merged = open(path_merged, encoding="utf-8").read()

# inline SERVICES and functions from _fix_all_services - read file and exec only functions
code = open("scripts/_fix_all_services.py", encoding="utf-8").read()
code = code.split("RELATED_PATTERN")[0]
ns = {}
exec(code, ns)
related_block = ns["related_block"]

slug = "monitoramento-de-qualidade-do-ar"
new_block = related_block(slug)
replacement = '<div class=\\"container\\">\\n        ' + new_block + '\\n    </div>\\n<script>'
PATTERN = re.compile(
    r'<div class=\\"container\\">\\n\s*<div class=\\"serv-inc__related\\">.*?</div>\s*\\n\s*</div>\s*\\n<script>',
    re.DOTALL,
)
updated, _ = PATTERN.subn(replacement, merged, count=1)
line = updated.split("\n")[6]
print("line6 len", len(line))
print("around 8780:", repr(line[8760:8820]))

# scan for " not preceded by odd backslashes
start = line.index('const content = "') + len('const content = "')
for i in range(start, min(len(line), start + 9000)):
    if line[i] == '"':
        bs = sum(1 for k in range(i - 1, max(start - 1, i - 10), -1) if line[k] == "\\")
        # proper: even number of consecutive backslashes before quote means unescaped
        back = 0
        j = i - 1
        while j >= start and line[j] == "\\":
            back += 1
            j -= 1
        if back % 2 == 0:
            print("BAD quote at", i - start, "from content start:", repr(line[i - 30 : i + 30]))
            break
