import logging

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.client.default import DefaultBotProperties

from data.config import BOT_TOKEN

from .db.crud.user import delete_user_with_
from .db.crud.mailing import get_mailing_by_
from .db.crud.weather_provider_info import get_weather_provider_info_by_
from .weather.parsing import get_information_about_weather_by_


async def send_mailing(user_chat_id: int, user_locale: str):
    """Sends the mailing to user with the given chat id."""
    temp_bot = Bot(
        token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
    )
    mailing = get_mailing_by_(user_chat_id)
    weather_provider_info = get_weather_provider_info_by_(mailing.id_user_id)

    try:
        information_about_weather = get_information_about_weather_by_(
            data={
                "lang_code": user_locale,
                "time_title": mailing.time_title,
                "city": weather_provider_info.city,
                "time": weather_provider_info.time,
                "type": weather_provider_info.type,
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
            user_chat_id,
            "Error :(",
            disable_notification=mailing.mute,
        )
        # await send_to_admin(error_message)
    finally:
        await temp_bot.session.close()
        del temp_bot
