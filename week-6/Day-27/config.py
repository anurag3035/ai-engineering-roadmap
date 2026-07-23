import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.5-flash"
)

MAX_MESSAGES = 10

SUMMARY_TRIGGER = 8

SESSION_FOLDER = "sessions"