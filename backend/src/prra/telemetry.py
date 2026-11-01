"""OpenTelemetry bootstrap: PRRA observes itself from day one (NFR-10)."""

from fastapi import FastAPI
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from prra import __version__
from prra.config import Settings


def configure_telemetry(app: FastAPI, settings: Settings) -> TracerProvider:
    resource = Resource.create(
        {
            "service.name": settings.service_name,
            "service.version": __version__,
            "deployment.environment": settings.environment,
        }
    )
    provider = TracerProvider(resource=resource)
    if settings.otlp_endpoint:
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otlp_endpoint)))
    # Pass the provider explicitly (no global state) so tests can build many apps.
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider, excluded_urls="healthz,readyz")
    return provider
