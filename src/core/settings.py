from functools import lru_cache

from pydantic_settings import BaseSettings


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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
