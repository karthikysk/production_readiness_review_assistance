from pathlib import Path

import pytest

from tests.architecture.rules import check_source, scan

SRC = Path(__file__).parents[2] / "src"
MODULES = ["review", "design", "blueprint", "checks", "remediation", "evidence", "identity", "notifications"]


def test_codebase_respects_module_boundaries() -> None:
    violations = scan(SRC)
    assert violations == [], "\n".join(f"{v.file} imports {v.imported}: {v.rule}" for v in violations)


@pytest.mark.parametrize("module", MODULES)
def test_every_module_has_public_interface_and_routes(module: str) -> None:
    base = SRC / "prra" / "modules" / module
    for required in ("__init__.py", "public.py", "api.py"):
        assert (base / required).exists(), f"{module} is missing {required}"


# --- the rules themselves must catch violations (tests of the test) -------------------------


def test_detects_deep_cross_module_import() -> None:
    src = "from prra.modules.design.service import extract\n"
    got = check_source(src, "prra.modules.review.service")
    assert [v.rule for v in got] == ["cross-module import must go through prra.modules.design.public"]


def test_allows_public_cross_module_import() -> None:
    src = "from prra.modules.design.public import GraphId\n"
    assert check_source(src, "prra.modules.review.service") == []


def test_allows_import_inside_same_module_including_relative() -> None:
    src = "from .models import Review\nfrom prra.modules.review.models import Review as R\n"
    assert check_source(src, "prra.modules.review.service") == []


def test_relative_import_escaping_module_is_caught() -> None:
    src = "from ..design import service\n"
    got = check_source(src, "prra.modules.review.service")
    assert got, "relative import into another module must be flagged"


def test_shared_must_not_import_modules() -> None:
    got = check_source("import prra.modules.review.public\n", "prra.shared.ids")
    assert [v.rule for v in got] == ["shared must not import modules or main"]


def test_modules_must_not_import_main() -> None:
    got = check_source("from prra.main import create_app\n", "prra.modules.checks.service")
    assert any("composition root" in v.rule for v in got)
