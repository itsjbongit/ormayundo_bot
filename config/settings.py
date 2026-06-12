import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
FIREBASE_KEY_PATH = "firebase_key.json"
DEFAULT_TIMEZONE = "Asia/Kolkata"  # Default fallback timezone