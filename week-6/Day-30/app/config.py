import os

from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.5-flash"
)

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        30
    )
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///chat.db"
)


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")