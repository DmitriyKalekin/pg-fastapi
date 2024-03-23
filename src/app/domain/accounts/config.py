from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    APP_ENV: str
    # ------------------------------
    POSTGRES_DBN: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"


@lru_cache()
def get_config():
    return Config()  # pragma: no cover


AConfig = Annotated[Config, Depends(get_config)]
