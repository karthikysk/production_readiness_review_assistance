from fastapi.testclient import TestClient


def test_liveness(client: TestClient) -> None:
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_readiness(client: TestClient) -> None:
    assert client.get("/readyz").json() == {"status": "ready"}


def test_meta_lists_all_modules(client: TestClient) -> None:
    body = client.get("/api/v1/meta").json()
    assert body["environment"] == "test"
    assert body["modules"] == [
        "blueprint",
        "checks",
        "design",
        "evidence",
        "identity",
        "notifications",
        "remediation",
        "review",
    ]


def test_openapi_is_published(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 200
