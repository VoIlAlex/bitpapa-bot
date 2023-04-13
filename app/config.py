import os

from pydantic import BaseConfig


class Config(BaseConfig):
    POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "bitpapa_bot")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_URL_SYNC = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_DB_TEST: str = os.getenv("POSTGRES_DB_TEST", "bitpapa_bot_test")
    POSTGRES_URL_TEST = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}"
    POSTGRES_URL_SYNC_TEST = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_TEST}"

    JWT_ALGORITHM: str = "HS256"
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY", "refresh_secret_key_123_qwe")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 10
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key_123_qwe")


config = Config()
