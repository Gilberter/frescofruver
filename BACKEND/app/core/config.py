from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Security
    SECRET_KEY: str = "dev-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    REFRESH_TOKEN_EXPIRE_DAYS: int = 10

    # App
    APP_ENV: str = "development"
    APP_TITLE: str = "FrescoExpress API"
    APP_VERSION: str = "1.0.0"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def is_dev(self) -> bool:
        return self.APP_ENV == "development"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

print(settings.DATABASE_URL)