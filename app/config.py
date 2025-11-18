from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    ENV: str = "dev"
    SERVICE_PORT: int = 8100
    TOKEN_TTL_SECONDS: int = 900
    LOG_JSON: bool = True
    SIGNING_ALG: str = "HS256"
    MASTER_SECRET: str = "CHANGE_ME"  # replace in .env

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
