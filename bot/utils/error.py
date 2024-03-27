import logging
from typing import Union

from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from .admins import send_to_admins


async def send_message_about_error(
    event: Union[Message, CallbackQuery],
    error: str,
    error_place: str = "",
    message_to_user: bool = True,
) -> None:
    """Sends the given error message to the admins (and user) and logs it."""
    if message_to_user:
        await _send_message_to_user_about_error(event)

    user = event.from_user
    reason = (
        f"message: '{event.text}'"
        if isinstance(event, Message)
        else f"clicking '{event.data}' on message\n---\n{event.message.text}"
    )
    error_message = (
        f"<b>Exception{error_place}</b> "
        f"with user <code>{user.id}</code> (@{user.username})\n\n"
        f"{error.capitalize()}\n\nafter {reason}"
    )
    logging.error(error.capitalize())
    await send_to_admins(error_message)


async def _send_message_to_user_about_error(
    event: Union[Message, CallbackQuery]
):
    """Sends the default message to user about error."""
    try:
        message_text = _(
            "An error occurred! :(\n"
            "Please, try again or restart the bot with the /start command."
        )
    except LookupError:
        logging.warning(
            "LookupError in the send_message_to_user_about_error function!"
        )
        message_text = (
            "An error occurred! :(\n"
            "Please, try again or restart the bot with the /start command."
        )
    await event.answer(message_text)
