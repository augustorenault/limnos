import glob
import re


def merge_content_string(text: str) -> str:
    lines = text.split("\n")
    start = next((i for i, line in enumerate(lines) if line.startswith('const content = "')), None)
    if start is None:
        return text
    end = start
    while end < len(lines) and not lines[end].rstrip().endswith('";'):
        end += 1
    if end >= len(lines):
        return text

    prefix = lines[start][: len('const content = "')]
    chunks = []
    for i in range(start, end + 1):
        chunk = lines[i]
        if i == start:
            chunk = chunk[len('const content = "'):]
        if i == end:
            chunk = chunk[: -len('";')]
        chunks.append(chunk)
    inner = "\\n".join(chunks)
    new_line = f'{prefix}{inner}";'
    return "\n".join(lines[:start] + [new_line] + lines[end + 1 :])


WS = r"(?:\\n| )*"

OLD_MPI_CTA = re.compile(
    rf'<div class=\\"position-relative container\\">{WS}'
    rf'<div class=\\"saiba-mais-mpi-10\\">{WS}'
    rf'<div class=\\"content-saiba-mais text-center\\">{WS}'
    rf'<h2 class=\\"light[^\\"]*\\">Entre em contato agora mesmo!</h2>{WS}'
    rf'<p class=[^>]*>Clique no botão e entre em contato[^<]*</p>{WS}'
    rf'<a[^>]*>Entre em contato</a>{WS}'
    rf'</div>{WS}</div>{WS}</div>',
    re.DOTALL,
)

NEW_CTA = (
    '<div class=\\"bg-cta-pattern cta-video d-flex align-items-center justify-content-center\\">\\n'
    '    <div class=\\"cta-video__media\\" aria-hidden=\\"true\\">'
    '<video class=\\"cta-video__video\\" src=\\"/video/banner-video.mp4\\" '
    'preload=\\"metadata\\" muted loop autoplay playsinline></video></div>\\n'
    '    <div class=\\"cta-video__veil\\" aria-hidden=\\"true\\"></div>\\n'
    '    <div class=\\"container text-center cta-video__inner\\">\\n'
    '        <div class=\\"d-flex flex-column justify-content-center align-items-center gap-3\\">\\n'
    '            <h2 class=\\"light m-0 fs-1\\">Entre em contato agora mesmo!</h2>\\n'
    '            <p class=\\"fs-4 light m-0\\">Clique no botão e entre em contato para tirar dúvidas ou solicitar um orçamento.</p>\\n'
    '            <div class=\\"d-flex justify-content-center align-items-center gap-2 flex-wrap\\">\\n'
    '                <a class=\\"btn btn--primary\\" href=\\"/contato\\" title=\\"Entre em contato\\">Entre em contato <i class=\\"ml-1 fas fa-envelope\\" aria-hidden=\\"true\\"></i></a>\\n'
    '                <a class=\\"btn btn--whatsapp\\" data-analytics rel=\\"nofollow\\" href=\\"https://wa.me/553185275215?text=Ol%C3%A1!%20Gostaria%20de%20mais%20informa%C3%A7%C3%B5es%20sobre%20as%20an%C3%A1lises%20da%20LIMNOS\\" target=\\"_blank\\" title=\\"WhatsApp LIMNOS\\">WhatsApp <i class=\\"ml-1 fab fa-whatsapp\\" aria-hidden=\\"true\\"></i></a>\\n'
    '            </div>\\n'
    '        </div>\\n'
    '    </div>\\n'
    '</div>'
)

INSERT_AFTER_ASIDE = re.compile(r'(</aside>\\n)(<div class=\\"clear\\"></div>)')


def transform(content: str) -> tuple[str, bool]:
    if "cta-video" in content and "saiba-mais-mpi-10" not in content:
        return content, False
    if "saiba-mais-mpi-10" not in content:
        return content, False

    new_content, removed = OLD_MPI_CTA.subn("", content, count=1)
    if removed != 1:
        return content, False

    if "cta-video" in new_content:
        return new_content, True

    if not INSERT_AFTER_ASIDE.search(new_content):
        return content, False

    new_content = INSERT_AFTER_ASIDE.sub(rf"\1{NEW_CTA}\\n\2", new_content, count=1)
    return new_content, True


skip = {"index", "contato", "obrigado", "empresa", "mapa-site", "informacoes"}
updated = 0
failed = []

for path in sorted(glob.glob("src/pages/**/index.astro", recursive=True)):
    norm = path.replace("\\", "/")
    if "/servicos/" in norm:
        continue
    slug = norm.split("/pages/")[1].replace("/index.astro", "")
    if slug in skip:
        continue

    with open(path, encoding="utf-8") as f:
        text = f.read()

    if 'const content = "' not in text:
        continue

    text = merge_content_string(text)
    start = text.index('const content = "') + len('const content = "')
    end = text.rindex('";')
    content = text[start:end]

    new_content, ok = transform(content)
    if not ok:
        failed.append(path)
        continue

    new_text = text[:start] + new_content + text[end:]
    new_text = merge_content_string(new_text)

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    updated += 1

print(f"updated: {updated}, failed: {len(failed)}")
if failed:
    print("failed:", failed[:5])
