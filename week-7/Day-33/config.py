import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-embedding-001"
)

CHROMA_DB_PATH = os.getenv(
    "CHROMA_DB_PATH",
    "./chroma_db"
)

QDRANT_PATH = os.getenv(
    "QDRANT_PATH",
    "./qdrant_db"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "documents"
)

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env")