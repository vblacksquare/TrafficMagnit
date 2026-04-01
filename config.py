
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Django(BaseModel):
    secret_key: str


class Redis(BaseModel):
    uri: str


class Database(BaseModel):
    name: str
    user: str
    password: str
    host: str


class Settings(BaseSettings):
    django: Django
    database: Database
    redis: Redis

    model_config = SettingsConfigDict(
        env_file=f".env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )


@lru_cache(maxsize=1)
def get_config() -> Settings:
    return Settings()
