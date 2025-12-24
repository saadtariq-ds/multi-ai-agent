""" Configuration settings for the application. """

import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    ALLOWED_MODELS_NAMES = [
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b"
    ]

settings = Settings()