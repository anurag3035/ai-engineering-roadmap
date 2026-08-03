from dotenv import load_dotenv
import os

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

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "documents"
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "10"
    )
)

RRF_K = int(
    os.getenv(
        "RRF_K",
        "60"
    )
)