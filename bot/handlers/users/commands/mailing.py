from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command(commands=["mailing"]))
async def handle_mailing_command(message: Message):
    """Handles the /mailing command."""
