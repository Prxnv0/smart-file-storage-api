from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    This keeps the project ready for AWS integration.
    """

    APP_NAME: str = Field("Smart File Storage & Processing System", description="Application name")
    APP_ENV: str = Field("local", description="Environment name (local/dev/prod)")

    # Storage backend selection: "local" or "s3"
    STORAGE_BACKEND: str = Field("local", description="Storage backend to use: local or s3")

    # Local storage (for development)
    LOCAL_UPLOAD_DIR: str = Field("./data/uploads", description="Local upload directory path")

    # AWS & DB placeholders for future integration
    AWS_REGION: str | None = Field(default=None, description="AWS region, e.g. us-east-1")
    S3_BUCKET_NAME: str | None = Field(default=None, description="Primary S3 bucket name")
    S3_PREFIX: str | None = Field(default=None, description="Optional S3 key prefix for uploads")

    DB_HOST: str | None = Field(default=None, description="Database hostname")
    DB_PORT: int | None = Field(default=None, description="Database port")
    DB_NAME: str | None = Field(default=None, description="Database name")
    DB_USER: str | None = Field(default=None, description="Database user")
    DB_PASSWORD: str | None = Field(default=None, description="Database password")

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
