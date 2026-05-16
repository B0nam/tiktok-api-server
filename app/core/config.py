from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    ms_tokens: str = ""
    proxy: Optional[str] = None
    headless: bool = True
    num_sessions: int = 3

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()