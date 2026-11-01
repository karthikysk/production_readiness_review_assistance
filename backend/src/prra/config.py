"""Application settings (12-factor: environment variables, prefix ``PRRA_``)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PRRA_", env_file=".env", extra="ignore")

    environment: str = "local"
    service_name: str = "prra-api"
    log_level: str = "INFO"
    # OpenTelemetry: when unset, spans are created but not exported.
    otlp_endpoint: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
