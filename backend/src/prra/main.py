"""Composition root: the only place that wires modules together."""

from fastapi import APIRouter, FastAPI

from prra import __version__
from prra.config import Settings, get_settings
from prra.modules.blueprint.api import router as blueprint_router
from prra.modules.checks.api import router as checks_router
from prra.modules.design.api import router as design_router
from prra.modules.evidence.api import router as evidence_router
from prra.modules.identity.api import router as identity_router
from prra.modules.notifications.api import router as notifications_router
from prra.modules.remediation.api import router as remediation_router
from prra.modules.review.api import router as review_router
from prra.shared.logging import configure_logging
from prra.telemetry import configure_telemetry

MODULE_ROUTERS: dict[str, APIRouter] = {
    "review": review_router,
    "design": design_router,
    "blueprint": blueprint_router,
    "checks": checks_router,
    "remediation": remediation_router,
    "evidence": evidence_router,
    "identity": identity_router,
    "notifications": notifications_router,
}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)
    app = FastAPI(title="PRRA API", version=__version__)

    @app.get("/healthz", tags=["ops"])
    def healthz() -> dict[str, str]:
        """Liveness: the process is up."""
        return {"status": "ok"}

    @app.get("/readyz", tags=["ops"])
    def readyz() -> dict[str, str]:
        """Readiness: dependencies reachable. (Database check arrives with the data layer.)"""
        return {"status": "ready"}

    api = APIRouter(prefix="/api/v1")

    @api.get("/meta", tags=["ops"])
    def meta() -> dict[str, object]:
        return {
            "name": settings.service_name,
            "version": __version__,
            "environment": settings.environment,
            "modules": sorted(MODULE_ROUTERS),
        }

    for router in MODULE_ROUTERS.values():
        api.include_router(router)
    app.include_router(api)

    configure_telemetry(app, settings)
    return app
