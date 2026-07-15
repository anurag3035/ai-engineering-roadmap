import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Default Gemini Model
MODEL_NAME = "gemini-1.5-flash"

# Generation Configuration
TEMPERATURE = 0.7
TOP_P = 0.95
TOP_K = 40
MAX_OUTPUT_TOKENS = 1024

# Maximum tokens allowed for a prompt
MAX_INPUT_TOKENS = 5000