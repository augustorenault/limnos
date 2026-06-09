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


COVER_PATTERN = re.compile(
    r'<div class=\\"col-md-8 col-12\\">\\n\s*'
    r'<div class=\\"service-inc__cover mb-5\\">\\n\s*'
    r'(.*?)\\n\s*</div>\\n\s*'
    r'</div>\\n\s*'
    r'<div class=\\"col-md-12 col-12\\">\\n\s*'
    r'(<h2 class=\\"my-0\\">.*?</h2>)\\n\s*'
    r'<div>\\n<div>',
    re.DOTALL,
)


def inline_cover(text: str) -> tuple[str, bool]:
    if "service-inc__cover--inline" in text:
        return text, False

    def repl(match: re.Match) -> str:
        cover_inner = match.group(1)
        heading = match.group(2)
        return (
            '<div class=\\"col-md-12 col-12 service-inc__content\\">\\n'
            f"                                {heading}\\n"
            '                                <div class=\\"service-inc__cover service-inc__cover--inline\\">\\n'
            f"                                    {cover_inner}\\n"
            "                                </div>\\n"
            '                                <div class=\\"service-inc__body\\">\\n<div>'
        )

    updated, count = COVER_PATTERN.subn(repl, text, count=1)
    return updated, count == 1


for path in sorted(glob.glob("src/pages/servicos/*/index.astro")):
    slug = path.replace("\\", "/").split("/servicos/")[1].split("/")[0]
    with open(path, encoding="utf-8") as f:
        text = f.read()

    text = merge_content_string(text)
    updated, ok = inline_cover(text)
    status = "inline" if ok else "merged"

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(updated)

    lines = updated.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith('const content = "'))
    end = start
    while end < len(lines) and not lines[end].rstrip().endswith('";'):
        end += 1
    print(f"ok {slug}: {status}, content_lines={end - start + 1}")

print("done")
