from typing import Any, Awaitable, Callable

from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class SchedulerMiddleware(BaseMiddleware):
    """Middleware for passing scheduler to handlers."""

    def __init__(self, scheduler: AsyncIOScheduler):
        """Calls the parent class constructor and sets the scheduler attribute."""
        super().__init__()
        self._scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """Passes the scheduler to the handler."""
        data["scheduler"] = self._scheduler
        return await handler(event, data)
