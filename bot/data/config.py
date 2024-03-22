import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [
    int(admin_chat_id) for admin_chat_id in str(os.getenv("ADMINS")).split(",")
]
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
SCHEDULER_JOBS_DATABASE_URL = os.getenv(
    "SCHEDULER_DATABASE_URL", SQLALCHEMY_DATABASE_URL
)

BASE_DIR = Path(__file__).parent.parent

LOCALES_DIR = BASE_DIR / "locales"
I18N_DOMAIN = os.getenv("I18N_DOMAIN", "messages")

DEFAULT_LOCALE = os.getenv("LOCALE", "en")
DEFAULT_TIMEZONE = os.getenv("TIMEZONE", "UTC")
