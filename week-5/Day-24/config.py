import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

print("Loaded MODEL_NAME:", MODEL_NAME)

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")