path = "src/pages/servicos/monitoramento-de-qualidade-do-ar/index.astro"
with open(path, encoding="utf-8") as f:
    lines = f.readlines()
line7 = lines[6]
print("line7 len", len(line7))
print("around 7621:", repr(line7[7600:7680]))
print("endswith", repr(line7[-80:]))
