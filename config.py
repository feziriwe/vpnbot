from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OUTLINE_API_URL = os.getenv("OUTLINE_API_URL")
OUTLINE_API_KEY = os.getenv("OUTLINE_API_KEY")