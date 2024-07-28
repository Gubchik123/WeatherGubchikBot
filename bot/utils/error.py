import logging
import traceback
from typing import Union

from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from utils.db.crud.user import get_user_by_
from keyboards.inline.profile.weather_provider import (
    get_weather_provider_inline_keyboard,
)

from .admins import send_to_admins


async def send_message_about_error(
    event: Union[Message, CallbackQuery],
    error: str,
    error_place: str = "",
    message_to_user: bool = True,
) -> None:
    """Sends the given error message to the admins (and user) and logs it."""
    logging.error(f"{error.capitalize()}{error_place}")
    await send_to_admins(
        get_admin_error_message(event, error, error_place),
        get_traceback_file_path(),
    )
    if message_to_user:
        await event.answer(get_user_error_message())


def get_admin_error_message(
    event: Union[Message, CallbackQuery], error: str, error_place: str
) -> str:
    """Returns the default admin error message."""
    user = event.from_user
    reason = (
        f"message: '{event.text}'"
        if isinstance(event, Message)
        else f"clicking '{event.data}' on message\n---\n{event.message.text}"
    )
    return (
        f"❗️ <b>Exception{error_place}</b> "
        f"with user <code>{user.id}</code> (@{user.username})\n\n"
        f"{error.capitalize()}\n\nafter {reason}"
    )


def get_traceback_file_path() -> str:
    """Returns the path to the file with traceback."""
    file_path = "traceback.txt"
    with open(file_path, "w") as file:
        traceback.print_exc(file=file)
    return file_path


def get_user_error_message() -> str:
    """Returns the default user error message."""
    try:
        return _(
            "An error occurred! 😥\n\n"
            "The admins have already been notified about this "
            "and will fix the problem as soon as possible.\n\n"
            "Please, try again or restart the bot with the /start command."
        )
    except LookupError:
        logging.warning("LookupError in the get_error_message function!")
        return (
            "An error occurred! 😥\n\n"
            "The admins have already been notified about this "
            "and will fix the problem as soon as possible.\n\n"
            "Please, try again or restart the bot with the /start command."
        )


async def send_weather_provider_server_error(
    message: Message, error: Exception
):
    """Sends weather provider server error."""
    user = get_user_by_(message.chat.id)
    reply_markup = (
        get_weather_provider_inline_keyboard(
            except_weather_provider=user.weather_provider
        )
        if user
        else None
    )
    await message.answer(
        _(
            "Unfortunately, the weather provider server is not available now. "
            "The error is not connected with the bot.\n\n"
            "Please, try again later <b>OR</b> choose another weather provider:"
        ),
        reply_markup=reply_markup,
    )
    await send_message_about_error(
        message,
        str(error),
        error_place=f" {str(error.__class__)[8:-2]}",
        message_to_user=False,
    )
