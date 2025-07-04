"""
Configuration loader for environment variables and constants.
- Loads .env securely using python-dotenv
- Raises clear error if OPENAI_API_KEY is missing
"""
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
