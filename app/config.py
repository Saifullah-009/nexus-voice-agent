import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    # Active production low-latency model
    LLM_MODEL = "gemini-3.5-flash-lite"

config = Config()