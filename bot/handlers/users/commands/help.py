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
            """
            Bot commands:
            /start - Start working with the bot
            /language - Change the language of the bot
            /help - Display of basic usage rules
            /weather - Display information about the weather
            /goodbye - Ending work with the bot

            Sign up for the newsletter to receive daily weather information in the city of your choice (you can turn it off at any time)

            I advise you to use the buttons for the intended result

            Enjoy using!!!

            Bot author contacts:
            CV site: https://nikita-hubariev.me
            LinkedIn: https://www.linkedin.com/in/nikita-hubariev
            Instagram: https://www.instagram.com/notwhale.1746

            Other projects of the author are available on:
            Project board: https://gubchik123-project-board.netlify.app
            GitHub: https://github.com/Gubchik123
            """.replace(
                "            ", ""
            )
        )
    )
