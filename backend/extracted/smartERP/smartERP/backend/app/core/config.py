"""Application configuration for SmartERP.

This module centralizes environment-driven settings so the rest of the
application can depend on a typed configuration object instead of raw
environment lookups.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings loaded from the backend .env file."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Core application metadata used by the FastAPI application object.
    app_name: str = Field(default="SmartERP API", validation_alias="SMARTERP_APP_NAME")
    app_version: str = Field(default="1.0.0", validation_alias="SMARTERP_APP_VERSION")

    # Database configuration is read from the environment for production deployments.
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/smartrp",
        validation_alias="SMARTERP_DATABASE_URL",
    )
    database_echo: bool = Field(default=False, validation_alias="SMARTERP_DB_ECHO")
    database_pool_size: int = Field(default=5, validation_alias="SMARTERP_DB_POOL_SIZE")
    database_max_overflow: int = Field(default=10, validation_alias="SMARTERP_DB_MAX_OVERFLOW")
    database_pool_recycle: int = Field(default=1800, validation_alias="SMARTERP_DB_POOL_RECYCLE")

    # CORS is configurable through the environment so frontends can vary by deployment.
    cors_allow_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        validation_alias="SMARTERP_CORS_ALLOW_ORIGINS",
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def parse_cors_allow_origins(cls, value: object) -> list[str]:
        """Normalize comma-separated CORS origins into a clean list."""

        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        return ["http://localhost:3000"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance for app-wide reuse."""

    return Settings()


# Export a module-level instance for code paths that prefer direct access.
settings = get_settings()