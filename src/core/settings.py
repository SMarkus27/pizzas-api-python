from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APPLICATION_HOST: str = "0.0.0.0"
    APPLICATION_PORT: int = 8000

    # MongoDB - conexão
    MONGODB_CONNECTION_URL: str

    # MongoDB - databases e collections
    MONGODB_DATABASE_NAME: str
    MONGODB_ORDER_COLLECTION: str
    MONGODB_PIZZA_COLLECTION: str
    MONGODB_STORE_COLLECTION: str

    MONGODB_DATABASE_TEST_NAME: str
    MONGODB_ORDER_TEST_COLLECTION: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
