from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./db/database.db"
    SECRET_KEY: str
    ALGORITHM: str
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
