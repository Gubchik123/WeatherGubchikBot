from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from utils.db.crud.user import get_user_by_
from keyboards.inline.profile import get_profile_inline_keyboard


router = Router()


@router.message(F.text.lower() == __("profile"))
@router.callback_query(F.data == "btn_profile")
async def handle_profile(event: Union[Message, CallbackQuery]) -> None:
    """Sends user profile menu."""
    is_callback_query = isinstance(event, CallbackQuery)
    message = event.message if is_callback_query else event
    user = get_user_by_(user_chat_id=message.chat.id)
    answer_method = message.edit_text if is_callback_query else message.answer

    await answer_method(
        _(
            "<b>Profile</b>\n\n"
            "Language: <i>{locale}</i>\n"
            "Timezone: <i>{timezone}</i>\n"
            "Weather provider: <i>{weather_provider}</i>\n\n"
            "Date you joined: <i>{created}</i>"
        ).format(
            locale=user.locale,
            timezone=user.timezone,
            weather_provider=user.weather_provider,
            created=user.created.strftime("%d.%m.%Y"),
        ),
        reply_markup=get_profile_inline_keyboard(),
    )
