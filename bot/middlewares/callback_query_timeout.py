from datetime import datetime
from typing import Optional, Dict, Any, Awaitable, Callable

from aiogram.types import CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class CallbackQueryTimeoutMiddleware(BaseMiddleware):
    """Middleware for passing scheduler to handlers."""

    def __init__(self, minutes: Optional[int] = 5):
        """Calls the parent class constructor and sets the scheduler attribute."""
        super().__init__()
        self._minutes = minutes

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        callback_query: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """Checks if the callback query message is older than the specified time."""
        if (
            callback_query.message.date.timestamp() + 60 * self._minutes
            < datetime.now().timestamp()
        ):
            await callback_query.answer("🕐")
            await callback_query.message.edit_text(
                callback_query.message.text, reply_markup=None
            )
            return
        return await handler(callback_query, data)
