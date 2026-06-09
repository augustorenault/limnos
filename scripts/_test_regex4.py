import re

SERVICES = [
    {"slug": "avaliacao-de-qualidade-da-agua-e-seus-organismos", "title": "Avaliação de Qualidade da Água e seus Organismos", "image": "/doutor/uploads/6/servicos/2025/04/cover-avaliacao-de-qualidade-da-agua-e-seus-organismos-fc65b43f29.webp", "description": "Análises e coletas em águas potáveis, residuais (efluentes), subterrâneas e superficiais em ambiente marinho e de água doce. Avaliação da qualidade da água e seus organismos."},
    {"slug": "avaliacao-de-residuos-e-solos", "title": "Avaliação de Materiais, Resíduos e Solos", "image": "/doutor/uploads/6/servicos/2025/04/cover-avaliacao-de-residuos-e-solos-cf21b43a04.webp", "description": "Caracterização de materiais, resíduos e solos para gerenciamento ambiental, conformidade legal e tomada de decisões seguras em projetos industriais e de infraestrutura."},
    {"slug": "monitoramento-de-emissoes-atmosfericas", "title": "Monitoramento de Emissões Atmosféricas", "image": "/doutor/uploads/6/servicos/2025/04/cover-monitoramento-de-emissoes-atmosfericas-f17a1dcb8e.webp", "description": "Avaliação de poluentes atmosféricos em chaminés e outras fontes de emissão, com dados confiáveis para gestão ambiental e atendimento à legislação."},
    {"slug": "monitoramento-de-qualidade-do-ar", "title": "Monitoramento de Qualidade do Ar", "image": "/doutor/uploads/6/servicos/2025/04/cover-monitoramento-de-qualidade-do-ar-14415ecda1.webp", "description": "Monitoramento de indicadores de qualidade do ar através de estações automáticas que analisam os níveis de concentrações de poluentes."},
    {"slug": "monitoramento-de-ruidos-e-vibracoes", "title": "Monitoramento de Ruídos e Vibrações", "image": "/doutor/uploads/6/servicos/2025/04/cover-monitoramento-de-ruidos-e-vibracoes-8cbbb129cf.webp", "description": "Análises de níveis de ruído e vibração do meio ambiente. Medições acústicas em ambientes internos e externos. Avaliação de poluição sonora."},
]

def card(service):
    title = service["title"]
    slug = service["slug"]
    image = service["image"]
    description = service["description"]
    return (
        '                                    <div class=\\"col-12 col-md-6 col-lg-3 pb-4 card-dr-pattern\\">\\n'
        '                        <div class=\\"card rounded rounded-3 p-2\\">\\n'
        '                            <div class=\\"card-dr-pattern-img\\">\\n\\n'
        f'                                <a href=\\"/servicos/{slug}\\" title=\\"{title}\\">\\n'
        f'                                    <img class=\\"card-img-top border rounded object-fit-contain\\" src=\\"{image}\\" alt=\\"{title}\\" title=\\"{title}\\">\\n'
        '                                </a>\\n'
        '                            </div>\\n'
        '                                <div class=\\"card-body p-1 m-0\\">\\n'
        '                                <div class=\\"fs-6 my-0\\">\\n'
        '                                                                        <a class=\\"category-related\\" href=\\"/servicos\\" title=\\"Serviços\\">Serviços</a>\\n'
        '                                </div>\\n'
        f'                                <h2 class=\\"mb-4 mt-3 card-title fs-5 text-uppercase fw-bold\\">{title}</h2>\\n'
        '                                                                    <p class=\\"card__description\\">\\n'
        f'                                                                                    {description}                                                                            </p>\\n'
        f'                                                                <a href=\\"/servicos/{slug}\\" class=\\"btn-link btn-link--primary\\" title=\\"{title}\\">\\n'
        '                                    Saiba Mais\\n'
        '                                </a>\\n'
        '                            </div>\\n'
        '                        </div>\\n'
        '                    </div>'
    )

def related_block(exclude_slug):
    cards = "".join(card(s) for s in SERVICES if s["slug"] != exclude_slug)
    return (
        '<div class=\\"serv-inc__related\\">\\n'
        '            <h2 class=\\"title-subtitle text-center fs-2 my-5\\"><span>Confira Também</span>Nossos Outros Serviços</h2>\\n'
        '            <div class=\\"row justify-content-center align-items-start\\">\\n'
        f'{cards}\\n'
        '                            </div>\\n'
        '        </div>'
    )

path = "scripts/_test_merged.astro"
merged = open(path, encoding="utf-8").read()
slug = "monitoramento-de-qualidade-do-ar"
new_block = related_block(slug)
replacement = '<div class=\\"container\\">\\n        ' + new_block + '\\n    </div>\\n<script>'
print("new_block real NL", new_block.count("\n"))
print("replacement real NL", replacement.count("\n"))

PATTERN = re.compile(
    r'<div class=\\"container\\">\\n\s*<div class=\\"serv-inc__related\\">.*?</div>\s*\\n\s*</div>\s*\\n<script>',
    re.DOTALL,
)
updated, count = PATTERN.subn(replacement, merged, count=1)
print("count", count, "lines", len(updated.split("\n")))
for i, line in enumerate(updated.split("\n")):
    if i > 5 and i < 15:
        print("line", i, "len", len(line), "prefix", line[:60])

# write and try build on single file - skip
