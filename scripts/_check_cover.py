path = "src/pages/servicos/monitoramento-de-qualidade-do-ar/index.astro"
lines = open(path, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith('const content = "'))
end = start
while end < len(lines) and not lines[end].rstrip().endswith('";'):
    end += 1
print("content lines", end - start + 1)
text = open(path, encoding="utf-8").read()
print("has inline cover", "service-inc__cover--inline" in text)
print("has old col-md-8", 'col-md-8 col-12' in text)
idx = text.find("service-inc__cover--inline")
print(text[idx - 100 : idx + 400])
