import importlib.util

spec = importlib.util.spec_from_file_location("fix", "scripts/_fix_all_services.py")
fix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix)

slug = "monitoramento-de-qualidade-do-ar"
new_block = fix.related_block(slug)
replacement = '<div class=\\"container\\">\\n        ' + new_block + '\\n    </div>\\n<script>'

print("new_block len", len(new_block))
print("real newlines in new_block", new_block.count("\n"))
print("escaped backslash-n in new_block", new_block.count("\\n"))
print("real newlines in replacement", replacement.count("\n"))

# show first chars with ord
for i, c in enumerate(new_block[:200]):
    if c == "\n":
        print("REAL NL at", i)
