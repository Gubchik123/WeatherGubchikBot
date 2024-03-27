from typing import Optional, Callable

from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def command_argument_required(convert: Optional[type] = str) -> Callable:
    def wrapper(command_handler: Callable) -> None:
        async def decorator(
            message: Message, scheduler: AsyncIOScheduler
        ) -> None:
            try:
                command_argument = convert(message.text.strip().split(" ")[1])
                try:
                    await command_handler(message, scheduler, command_argument)
                except TypeError:
                    await command_handler(message, command_argument)
            except IndexError:
                await message.answer("<b>Command argument is required!</b>")
            except ValueError:
                await message.answer(
                    "<b>Invalid type of the given command argument!</b> "
                    f"Expected: <i>{convert.__name__}</i>."
                )

        return decorator

    return wrapper
