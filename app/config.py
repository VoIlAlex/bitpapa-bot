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

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    JWT_ALGORITHM: str = "HS256"
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY", "refresh_secret_key_123_qwe")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 10
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key_123_qwe")

    BITPAPA_TOKEN = os.getenv("BITPAPA_TOKEN")

    MESSAGE_GREETING_DEFAULT_TEMPLATE = "Hi! I'm the bot."
    MESSAGE_BILL_DEFAULT_TEMPLATE = "Your bill: {bill_url}."
    MESSAGE_PAYMENT_FAILED = "Payment failed."
    MESSAGE_PAID_TEMPLATE = "Your payment was approved. Please, wait."
    MESSAGE_WRONG_PHONE_FORMAT = "Wrong phone format."
    MESSAGE_PHONE_SUCCESS = "Phone information saved."

    ALLOWED_PAYMENT_METHOD_CODES = ["QIWI"]

    QIWI_BILL_EXPIRATION_DELTA = 1 * 60 * 60
    QIWI_SITE_ID = os.getenv("QIWI_SITE_ID")
    QIWI_TOKEN = os.getenv("QIWI_TOKEN")


config = Config()
