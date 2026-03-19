from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.i18n import I18n

from data.config import BOT_TOKEN, I18N_DOMAIN, LOCALES_DIR, DEFAULT_LOCALE


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML"),
)

i18n = I18n(
    path=LOCALES_DIR, default_locale=DEFAULT_LOCALE, domain=I18N_DOMAIN
)
