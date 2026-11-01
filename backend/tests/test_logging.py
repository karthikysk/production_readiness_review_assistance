import json
import logging

from opentelemetry.sdk.trace import TracerProvider

from prra.shared.logging import JsonFormatter


def _record(msg: str) -> logging.LogRecord:
    return logging.LogRecord("t", logging.INFO, __file__, 1, msg, None, None)


def test_json_log_has_core_fields() -> None:
    data = json.loads(JsonFormatter().format(_record("hello")))
    assert data["message"] == "hello"
    assert data["level"] == "INFO"
    assert "trace_id" not in data


def test_json_log_is_correlated_with_active_trace() -> None:
    tracer = TracerProvider().get_tracer("test")
    with tracer.start_as_current_span("s") as span:
        data = json.loads(JsonFormatter().format(_record("in span")))
        assert data["trace_id"] == f"{span.get_span_context().trace_id:032x}"
