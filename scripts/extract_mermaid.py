"""Extract every ```mermaid block from Markdown files into an output directory.

Usage: python scripts/extract_mermaid.py OUT_DIR
Each block becomes a .mmd file so it can be rendered/validated with mermaid-cli.
"""

import pathlib
import re
import sys

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
root = pathlib.Path(".")
count = 0
for md in sorted([*root.glob("*.md"), *root.glob("docs/**/*.md")]):
    for i, m in enumerate(
        re.finditer(r"```mermaid\n(.*?)```", md.read_text(), re.DOTALL), 1
    ):
        count += 1
        (out / f"{str(md).replace('/', '__')}__{i}.mmd").write_text(m.group(1))
print(f"extracted {count} diagrams")
