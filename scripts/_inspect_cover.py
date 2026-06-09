import re

text = open("src/pages/servicos/monitoramento-de-qualidade-do-ar/index.astro", encoding="utf-8").read()
start = text.index('const content = "') + len('const content = "')
end = text.rindex('";')
c = text[start:end]
i = c.find("service-inc__cover")
print(c[i - 250 : i + 700])
print("---END---")
j = c.find("</div>\n</div>\n                            </div>", i)
print(c[j : j + 200])
