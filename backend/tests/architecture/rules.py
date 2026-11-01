"""Static import analysis used by the architecture fitness tests (ADR-0002).

Rules
1. A module may import another module only through ``prra.modules.<other>.public``.
2. ``prra.shared`` must not import ``prra.modules`` or ``prra.main``.
3. Modules must not import ``prra.main`` (the composition root).
"""

import ast
from dataclasses import dataclass
from pathlib import Path

PKG = "prra"
MODULES_PREFIX = f"{PKG}.modules."


@dataclass(frozen=True)
class Violation:
    file: str
    imported: str
    rule: str


def module_name(path: Path, src_root: Path) -> str:
    rel = path.relative_to(src_root).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def imported_names(source: str, current_module: str, is_package: bool) -> list[str]:
    """Return absolute dotted names imported by ``source`` (relative imports resolved)."""
    tree = ast.parse(source)
    base = current_module.split(".")
    pkg_parts = base if is_package else base[:-1]
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                anchor = pkg_parts[: len(pkg_parts) - (node.level - 1)]
                mod = ".".join([*anchor, node.module] if node.module else anchor)
            else:
                mod = node.module or ""
            found.append(mod)
            # "from prra.modules.x import y" may import a submodule named y
            found.extend(f"{mod}.{alias.name}" for alias in node.names)
    return found


def owning_module(name: str) -> str | None:
    if name.startswith(MODULES_PREFIX):
        return name[len(MODULES_PREFIX) :].split(".")[0]
    return None


def check_source(source: str, current_module: str, is_package: bool = False) -> list[Violation]:
    found: dict[tuple[str, str], Violation] = {}
    me = owning_module(current_module)
    in_shared = current_module == f"{PKG}.shared" or current_module.startswith(f"{PKG}.shared.")

    def add(imported: str, rule: str) -> None:
        # Report each offending module once, not once per imported name.
        key = (".".join(imported.split(".")[:4]), rule)
        found.setdefault(key, Violation(current_module, key[0], rule))

    for imp in imported_names(source, current_module, is_package):
        parts = imp.split(".")
        if in_shared and (imp.startswith(f"{PKG}.modules") or imp == f"{PKG}.main"):
            add(imp, "shared must not import modules or main")
        if me is None:
            continue
        if imp == f"{PKG}.main":
            add(imp, "modules must not import the composition root")
        other = owning_module(imp)
        if other and other != me and len(parts) > 3 and parts[3] != "public":
            add(imp, f"cross-module import must go through prra.modules.{other}.public")
    return list(found.values())


def scan(src_root: Path) -> list[Violation]:
    out: list[Violation] = []
    for path in sorted((src_root / PKG).rglob("*.py")):
        name = module_name(path, src_root)
        out.extend(check_source(path.read_text(), name, is_package=path.name == "__init__.py"))
    return out
