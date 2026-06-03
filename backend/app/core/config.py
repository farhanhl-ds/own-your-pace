from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "own-your-pace"
    app_version: str = "0.1.0"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost"]

    # Database
    database_url: str

    # Redis
    redis_url: str

    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    # Strava
    strava_client_id: str = ""
    strava_client_secret: str = ""
    strava_webhook_verify_token: str = ""

    # Internal
    internal_api_key: str = ""

    # Storage
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 50


@lru_cache
def get_settings() -> Settings:
    return Settings()
