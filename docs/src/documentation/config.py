from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_measurement_id: str = ""


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
