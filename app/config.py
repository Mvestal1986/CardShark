import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tcgscan")
    USE_REMOTE_ML: bool = os.getenv("USE_REMOTE_ML", "false").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-prod")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
