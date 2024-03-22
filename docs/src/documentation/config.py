from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel as BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    google_measurement_id: str = ""


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
