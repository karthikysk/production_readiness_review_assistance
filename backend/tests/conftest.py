from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from prra.config import Settings
from prra.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app(Settings(environment="test", log_level="WARNING"))
    with TestClient(app) as c:
        yield c
