import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Model
MODEL_NAME = "gemini-1.5-flash"

# Generation Configuration
TEMPERATURE = 0.2
TOP_P = 0.95
TOP_K = 40
MAX_OUTPUT_TOKENS = 1024

# Prompt Directory
PROMPTS_DIR = "prompts"