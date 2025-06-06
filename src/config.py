from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_USER: str
    DB_HOST: str

    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    SENDER_PASSWORD: str
    EMAIL: str

    CLIENT_ID: str

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")



print(f"Loading env file from: '.env'")

settings = Settings()
print(f"ACCESS_TOKEN_EXPIRE_MINUTES={settings.ACCESS_TOKEN_EXPIRE_MINUTES}")





