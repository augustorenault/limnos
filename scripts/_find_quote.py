import re

# load test_regex4 logic minimally
exec(open("scripts/_test_regex4.py", encoding="utf-8").read().split("path = ")[0])

merged = open("scripts/_test_merged.astro", encoding="utf-8").read()
slug = "monitoramento-de-qualidade-do-ar"
new_block = related_block(slug)
replacement = '<div class=\\"container\\">\\n        ' + new_block + '\\n    </div>\\n<script>'
PATTERN = re.compile(
    r'<div class=\\"container\\">\\n\s*<div class=\\"serv-inc__related\\">.*?</div>\s*\\n\s*</div>\s*\\n<script>',
    re.DOTALL,
)
updated, _ = PATTERN.subn(replacement, merged, count=1)
line = updated.split("\n")[6]
# find first unescaped double-quote after const content = "
start = line.index('const content = "') + len('const content = "')
i = start
while i < len(line):
    if line[i] == '"':
        # count preceding backslashes
        bs = 0
        j = i - 1
        while j >= 0 and line[j] == "\\":
            bs += 1
            j -= 1
        if bs % 2 == 0:
            print("unescaped quote at", i, "context:", repr(line[i - 40 : i + 40]))
            break
    i += 1
