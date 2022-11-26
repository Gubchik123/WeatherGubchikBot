import os
from dotenv import load_dotenv


load_dotenv()

DB_URI = str(os.getenv("DB_URI"))
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
