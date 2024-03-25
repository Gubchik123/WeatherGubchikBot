from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _


router = Router()


@router.message(Command(commands=["help"]))
async def handle_help_command(message: Message):
    """Handles the /help command."""
    await message.answer(
        _(
            "Bot commands:\n"
            "/start - Start working with the bot\n"
            "/help - Get basic usage rules\n"
            "/weather - Get weather forecast\n"
            "/profile - Get user profile\n"
            "/mailing - Get mailing menu / Sign up for the newsletter\n"
            "/goodbye - Pause working with the bot\n\n"
            "Sign up for the newsletter (/mailing) to receive daily weather information in the city of your choice (you can turn it off at any time)\n\n"
            "I advise you to use the buttons or commands for the intended result\n\n"
            "Enjoy using!!!\n\n"
            "Bot author contacts:\n"
            "CV site: https://nikita-hubariev.me\n"
            "LinkedIn: https://www.linkedin.com/in/nikita-hubariev\n"
            "Instagram: https://www.instagram.com/notwhale.1746\n\n"
            "Other projects of the author are available on:\n"
            "Project board: https://gubchik123-project-board.netlify.app\n"
            "GitHub: https://github.com/Gubchik123\n"
        )
    )
