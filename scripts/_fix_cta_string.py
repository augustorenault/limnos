import glob

CTA_BLOCK = (
    '<div class=\\"bg-cta-pattern cta-video d-flex align-items-center justify-content-center\\">\\n'
    '    <div class=\\"cta-video__media\\" aria-hidden=\\"true\\">'
    '<video class=\\"cta-video__video\\" src=\\"/video/banner-video.mp4\\" '
    'preload=\\"metadata\\" muted loop autoplay playsinline></video></div>\\n'
    '    <div class=\\"cta-video__veil\\" aria-hidden=\\"true\\"></div>\\n'
    '    <div class=\\"container text-center cta-video__inner\\">\\n'
)


def fix_file(path: str) -> bool:
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    start = next((i for i, line in enumerate(lines) if line.startswith('const content = "')), None)
    if start is None:
        return False

    end = start
    while end < len(lines) and not lines[end].rstrip().endswith('";'):
        end += 1
    if end >= len(lines):
        return False

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

    # Normalize CTA block and hero video src.
    import re

    inner = re.sub(
        r'</div>\\n<div class=\\"bg-cta-pattern cta-video d-flex align-items-center justify-content-center\\">\\n\s*'
        r'<div class=\\"cta-video__media\\"[^>]*>.*?</video></div>\\n\s*'
        r'<div class=\\"cta-video__veil\\"[^>]*></div>\\n\s*'
        r'<div class=\\"container text-center cta-video__inner\\">\\n',
        CTA_BLOCK,
        inner,
        flags=re.DOTALL,
    )
    old_static = (
        '<div class=\\"bg-cta-pattern d-flex align-items-center justify-content-center\\">\\n'
        '    <div class=\\"container text-center\\">\\n'
    )
    inner = inner.replace(old_static, CTA_BLOCK)
    inner = re.sub(
        r'(<video class=\\"cta-video__video\\" src=\\")[^\\"]+(\\")',
        r'\1/video/banner-video.mp4\2',
        inner,
    )

    new_line = f'{prefix}{inner}";'
    new_lines = lines[:start] + [new_line] + lines[end + 1 :]
    new_text = "\n".join(new_lines)
    old_text = "\n".join(lines)
    if new_text == old_text:
        return False

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)
    return True


for path in sorted(glob.glob("src/pages/servicos/*/index.astro")):
    if fix_file(path):
        print(f"fixed: {path}")

print("done")
