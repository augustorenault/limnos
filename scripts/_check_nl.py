code = open("scripts/_fix_all_services.py", encoding="utf-8").read().split("RELATED_PATTERN")[0]
ns = {}
exec(code, ns)
nb = ns["related_block"]("monitoramento-de-qualidade-do-ar")
rep = '<div class=\\"container\\">\\n        ' + nb + '\\n    </div>\\n<script>'
print("real NL in nb", nb.count("\n"))
print("real NL in rep", rep.count("\n"))
for i, c in enumerate(nb):
    if c == "\n":
        print("NL at", i, repr(nb[max(0, i - 25) : i + 25]))
