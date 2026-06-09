import glob

OLD = (
    "O conteúdo do texto desta página é de direito reservado. Sua reprodução, parcial ou total, "
    "mesmo citando nossos links, é proibida sem a autorização do autor. Crime de violação de "
    'direito autoral – artigo 184 do Código Penal – <a rel=\\"nofollow\\" '
    'href=\\"http://www.planalto.gov.br/Ccivil_03/Leis/L9610.htm\\" target=\\"_blank\\" '
    'title=\\"Lei de direitos autorais\\">Lei 9610/98 - Lei de direitos autorais</a>.'
)

NEW = (
    "Este conteúdo é de autoria da Limnos e está protegido pela legislação brasileira de "
    "direitos autorais. Caso deseje reproduzi-lo ou citá-lo, entre em contato conosco."
)

skip = {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}
updated = 0

for path in sorted(glob.glob("src/pages/**/index.astro", recursive=True)):
    norm = path.replace("\\", "/")
    if "/servicos/" in norm:
        continue
    slug = norm.split("/pages/")[1].replace("/index.astro", "")
    if slug in skip:
        continue

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if OLD not in text:
        continue

    text = text.replace(OLD, NEW, 1)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    updated += 1

print(f"updated: {updated}")
