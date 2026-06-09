import re
import importlib.util

spec = importlib.util.spec_from_file_location("fix", "scripts/_fix_all_services.py")
fix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix)

path = "scripts/_test_merged.astro"
text = open(path, encoding="utf-8").read()
slug = "monitoramento-de-qualidade-do-ar"

new_block = fix.related_block(slug)
replacement = '<div class=\\"container\\">\\n        ' + new_block + '\\n    </div>\\n<script>'
updated, count = fix.RELATED_PATTERN.subn(replacement, text, count=1)
print("regex count", count)
print("lines after regex", len(updated.split("\n")))
# check for physical newlines inside const content line
lines = updated.split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith('const content = "'))
print("content line index", start, "total lines", len(lines))
print("has real newline in content?", "\n" in lines[start] if len(lines) > start else "n/a")

# find unescaped quotes issue - look for pattern that breaks string
line = lines[start]
# position 8910 from error
if len(line) > 8910:
    print("around 8910:", repr(line[8880:8950]))
