from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Diet"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()