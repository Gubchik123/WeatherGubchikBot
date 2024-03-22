from typing import Dict, Any, Optional

from aiogram.types import TelegramObject, User as TelegramUser

from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from utils.db.crud.user import get_user_locale_by_


class LanguageMiddleware(SimpleI18nMiddleware):
    """Middleware for getting user language."""

    async def get_locale(
        self, event: TelegramObject, data: Dict[str, Any]
    ) -> str:
        """Returns user language code."""
        telegram_user_locale = await super().get_locale(event, data)
        telegram_user: Optional[TelegramUser] = data.get(
            "event_from_user", None
        )
        if telegram_user:
            return (
                get_user_locale_by_(telegram_user.id) or telegram_user_locale
            )
        return telegram_user_locale
