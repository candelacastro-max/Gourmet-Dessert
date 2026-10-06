# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str                     # Sin default — obligatorio
    SECRET_KEY: str                       # Sin default — obligatorio
    ALGORITHM: str = "HS256"
    ACCESS_MIN: int = 30                  # minutos de vida del access token
    REFRESH_MIN: int = 10080              # minutos de vida del refresh token (7 días)
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:3000,http://127.0.0.1:5173"

    class Config:
        env_file = ".env"

settings = Settings()
