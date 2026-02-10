import os


class Settings:
    POSTGRES_URL = os.getenv(
        "POSTGRES_URL", "postgresql+asyncpg://admin:admin@db:5432/emotion_chat"
    )
    HISTORY_KEY = "chat:messages"  # list of JSON strings
    HISTORY_LIMIT = 50
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
    MODEL_URL = os.getenv(
        "MODEL_URL",
        "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    )
    JWT_SECRET = "supersecretkey"
    JWT_ALGORITHM = "HS256"


settings = Settings()
