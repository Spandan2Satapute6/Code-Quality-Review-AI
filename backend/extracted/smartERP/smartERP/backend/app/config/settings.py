"""
Application settings for SmartERP Enterprise Edition.
"""

from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from .env"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------------
    # App
    # -------------------------
    app_name: str = Field(default="SmartERP Enterprise", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    debug: bool = Field(default=True, alias="DEBUG")

    # -------------------------
    # Database
    # -------------------------
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="smarterp_db", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")

    database_pool_size: int = Field(default=10, alias="DB_POOL_SIZE")
    database_max_overflow: int = Field(default=20, alias="DB_MAX_OVERFLOW")
    database_pool_recycle: int = Field(default=1800, alias="DB_POOL_RECYCLE")
    database_echo: bool = Field(default=False, alias="DB_ECHO")

    # -------------------------
    # JWT
    # -------------------------
    secret_key: str = Field(alias="JWT_SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30,
        alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    @property
    def database_url(self) -> str:
        password = quote_plus(self.db_password)

        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()