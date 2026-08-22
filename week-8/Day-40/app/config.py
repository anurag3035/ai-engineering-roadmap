import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-3.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret")
DB_PATH = os.getenv("DB_PATH", "rag_assistant.db")
