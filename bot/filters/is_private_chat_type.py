from aiogram.filters import Filter
from aiogram.types import Message


class IsPrivateChatType(Filter):
    """Filter for private chat type."""

    async def __call__(self, message: Message) -> bool:
        """Checks if the given message chat type is private."""
        return message.chat.type == "private"
