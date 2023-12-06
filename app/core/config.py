import secrets

from pydantic import AnyHttpUrl


class Settings:
    PROJECT_NAME: str = "DB Tester API"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ["*"]
    SQLITE_URI: str = "sqlite:///./my_database.db"
    SQLITE_AUTH_URL: str = "sqlite+aiosqlite:///./data/auth.db"


settings = Settings()
