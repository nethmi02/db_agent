import os
from dotenv import load_dotenv

# Load variables from the .env file if it exists
load_dotenv()

# We read the values and provide default fallbacks
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sample.db")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

# How many past messages the agent remembers
try:
    MEMORY_LIMIT = int(os.getenv("MEMORY_LIMIT", "10"))
except ValueError:
    MEMORY_LIMIT = 10

def validate_config():
    """Check if all required configuration is present."""
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing! "
            "Please add it to your .env file or environment variables."
        )
