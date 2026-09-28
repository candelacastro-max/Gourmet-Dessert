# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str                     # Sin default — obligatorio
    SECRET_KEY: str                       # Sin default — obligatorio
    ALGORITHM: str = "HS256"
    ACCESS_MIN: int = 30                  # minutos de vida del access token
    REFRESH_MIN: int = 10080              # minutos de vida del refresh token (7 días)

    class Config:
        env_file = ".env"

settings = Settings()
