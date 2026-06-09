merged = open("scripts/_test_merged.astro", encoding="utf-8").read()
line = merged.split("\n")[6]
print("line6 len", len(line))
print("real NL inside line6", line.count("\n"))

# count two-char backslash-n sequences
import re
bs_n = len(re.findall(r"\\n", line))
print("backslash-n sequences", bs_n)

# find real newlines inside line6
for i, c in enumerate(line):
    if c == "\n":
        print("REAL nl at", i)
