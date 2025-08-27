import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tcgscan")
    USE_REMOTE_ML: bool = os.getenv("USE_REMOTE_ML", "false").lower() == "true"

settings = Settings()
