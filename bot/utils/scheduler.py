import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.default import DefaultBotProperties

from data.config import BOT_TOKEN

from .admins import send_to_admins
from .weather import get_weather_provider_module_by_
from .db.crud.mailing import get_mailing_by_
from .db.crud.user import get_user_by_, delete_user_with_
from .error import (
    get_admin_error_message,
    get_traceback_file_path,
    get_user_error_message,
)


async def send_mailing(user_chat_id: int):
    """Sends the mailing to user with the given chat id."""
    temp_bot = Bot(
        token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
    )
    user = get_user_by_(user_chat_id)
    weather_provider_module = get_weather_provider_module_by_(
        user.weather_provider
    )
    mailing = get_mailing_by_(user.chat_id)

    message = await temp_bot.send_message(
        user_chat_id, "📨", disable_notification=mailing.mute
    )
    try:
        await temp_bot.send_message(
            user_chat_id,
            weather_provider_module.get_information_about_weather_by_(
                data={
                    "time_title": mailing.time_title,
                    "city": mailing.weather_provider_info.city,
                    "time": mailing.weather_provider_info.time,
                    "type": mailing.weather_provider_info.type,
                    "lang_code": user.locale,
                }
            ),
        )
    except TelegramForbiddenError:
        delete_user_with_(user_chat_id)
    except Exception as error:
        admin_error_message = get_admin_error_message(
            message,
            str(error),
            error_place=f" {str(error.__class__)[8:-2]} in daily mailing",
        )
        await send_to_admins(
            admin_error_message, get_traceback_file_path(), temp_bot=temp_bot
        )
        user_error_message = "\n\n".join(
            get_user_error_message().split("\n\n")[:-1]
        )
        await temp_bot.send_message(
            user_chat_id, user_error_message, disable_notification=mailing.mute
        )
    finally:
        await temp_bot.session.close()
        del temp_bot
