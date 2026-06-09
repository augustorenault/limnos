import re

text = open("src/pages/servicos/monitoramento-de-qualidade-do-ar/index.astro", encoding="utf-8").read()
start = text.index('const content = "') + len('const content = "')
end = text.rindex('";')
c = text[start:end]
# find text end before aside
idx = c.find("<p>A LIMNOS conta com equipe")
print(c[idx : idx + 400])
