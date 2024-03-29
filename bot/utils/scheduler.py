import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.default import DefaultBotProperties

from data.config import BOT_TOKEN

from .admins import send_to_admins
from .db.crud.mailing import get_mailing_by_
from .db.crud.user import get_user_locale_by_, delete_user_with_
from .weather.parsing import get_information_about_weather_by_


async def send_mailing(user_chat_id: int):
    """Sends the mailing to user with the given chat id."""
    temp_bot = Bot(
        token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
    )
    mailing = get_mailing_by_(user_chat_id)

    try:
        information_about_weather = get_information_about_weather_by_(
            data={
                "time_title": mailing.time_title,
                "city": mailing.weather_provider_info.city,
                "time": mailing.weather_provider_info.time,
                "type": mailing.weather_provider_info.type,
                "lang_code": get_user_locale_by_(user_chat_id),
            }
        )
        await temp_bot.send_message(
            user_chat_id, "📨", disable_notification=mailing.mute
        )
        await temp_bot.send_message(user_chat_id, information_about_weather)
    except TelegramForbiddenError:
        delete_user_with_(user_chat_id)
    except Exception as e:
        error_message = f"Exception in daily mailing (user chat id - {user_chat_id}): {str(e)}"
        logging.error(error_message)

        await temp_bot.send_message(
            user_chat_id, "Error :(", disable_notification=mailing.mute
        )
        await send_to_admins(error_message, temp_bot)
    finally:
        await temp_bot.session.close()
        del temp_bot
