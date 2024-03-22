from typing import Union, Dict, Any, Optional

from aiogram.utils.i18n.middleware import SimpleI18nMiddleware
from aiogram.types import Message, CallbackQuery, User as TelegramUser

from utils.db.crud.user import get_user_locale_by_


class LanguageMiddleware(SimpleI18nMiddleware):
    """Middleware for getting user language."""

    async def get_locale(
        self, event: Union[Message, CallbackQuery], data: Dict[str, Any]
    ) -> str:
        """Returns user language code."""
        try:
            if event.data.startswith(
                "btn_start_lang"
            ) or event.data.startswith("btn_menu_lang"):
                return event.data.split("_")[-1]
        except AttributeError:
            pass  # Event is Message and doesn't have 'data'

        telegram_user_locale = await super().get_locale(event, data)
        telegram_user: Optional[TelegramUser] = data.get(
            "event_from_user", None
        )
        if telegram_user:
            return (
                get_user_locale_by_(telegram_user.id) or telegram_user_locale
            )
        return telegram_user_locale
