from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./db/database.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
