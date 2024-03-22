from typing import Union

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS


class IsAdmin(Filter):
    """Filter for checking if user is admin."""

    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        """Returns True if user is admin and False otherwise."""
        return event.from_user.id in ADMINS
