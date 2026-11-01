"""Check that every relative Markdown link and heading anchor in the repo resolves.

Run from the repository root:  python scripts/check_docs.py
Exit code is 1 if any link is broken.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path.cwd()
FENCE = re.compile(r"```.*?```", re.DOTALL)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def slug(heading: str) -> str:
    """GitHub-style heading anchor."""
    text = re.sub(r"<[^>]+>", "", heading.replace("`", "")).strip().lower()
    return "".join(c for c in text if c.isalnum() or c in " -_").replace(" ", "-")


def markdown_files() -> list[pathlib.Path]:
    found = [
        *ROOT.glob("*.md"),
        *ROOT.glob("docs/**/*.md"),
        *ROOT.glob(".github/**/*.md"),
    ]
    return sorted(p for p in found if p.is_file())


def main() -> int:
    files = markdown_files()
    anchors = {
        f: {slug(m.group(2)) for m in HEADING.finditer(FENCE.sub("", f.read_text()))}
        for f in files
    }
    broken = 0
    for f in files:
        for m in LINK.finditer(FENCE.sub("", f.read_text())):
            link = m.group(1)
            if link.startswith(("http", "mailto:", "../../issues")):
                continue
            path, _, anchor = link.partition("#")
            target = (f.parent / path).resolve() if path else f
            rel = f.relative_to(ROOT)
            if path and not target.exists():
                print(f"MISSING  {rel}: {link}")
                broken += 1
            elif (
                anchor
                and target.suffix == ".md"
                and anchor not in anchors.get(target, set())
            ):
                print(f"ANCHOR   {rel}: {link}")
                broken += 1
    print(f"{broken} broken link(s) in {len(files)} files")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
