from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from bot import bot
from utils.decorators import before_handler_clear_state
from data.config import WEATHER_PROVIDERS, LANGUAGES, MAILING_TIMES


router = Router()


@router.message(Command("help"))
@before_handler_clear_state
async def handle_help_command(message: Message, **kwargs):
    """Handles the /help command."""
    (
        await _send_private_help_message(message)
        if message.chat.type == "private"
        else await _send_group_help_message(message)
    )


async def _send_private_help_message(message: Message):
    """Sends a private help message."""
    await message.answer(
        _(
            "Bot commands:\n"
            "/start - Start working with the bot\n"
            "/help - Get basic usage rules\n"
            "/menu - Get main menu\n"
            "/moon - Get moon phase\n"
            "/weather ([language code: {languages}] "
            "[weather provider: {providers}] [city] [period]) "
            "- Get weather forecast\n"
            "/profile - Get user profile\n"
            "/mailing ([language code: {languages}] "
            "[weather provider: {providers}] [city] [period] [time: {times}] "
            "[mute: True (t,1) / False (f,0)]) "
            "- Get mailing menu / Sign up for or update the newsletter\n"
            "/goodbye - Pause working with the bot\n\n"
            "Sign up for the newsletter (/mailing) to receive daily weather information in the city of your choice (you can turn it off at any time)\n\n"
            "I advise you to use the buttons or commands for the intended result\n\n"
            "Enjoy using!!!\n\n"
            "You can suggest an idea or report a bug by following the link: "
            "https://github.com/Gubchik123/WeatherGubchikBot/issues/new\n\n"
            "Bot author contacts:\n"
            "CV site: https://hubariev.com\n"
            "LinkedIn: https://www.linkedin.com/in/nikita-hubariev\n"
            "Instagram: https://www.instagram.com/notwhale.1746\n\n"
            "Other projects of the author are available on:\n"
            "Portfolio: https://portfolio.hubariev.com\n"
            "GitHub: https://github.com/Gubchik123\n"
        ).format(
            languages=", ".join(LANGUAGES),
            providers=", ".join(WEATHER_PROVIDERS),
            times=", ".join(map(str, MAILING_TIMES)),
        )
    )


async def _send_group_help_message(message: Message):
    """Sends a group help message."""
    bot_me = await bot.get_me()
    await message.answer(
        _(
            "{bot_username} commands:\n"
            "/help@{bot_username} - Get basic usage rules\n"
            "/moon@{bot_username} - Get moon phase\n"
            "/weather@{bot_username} [language code: {languages}] "
            "[weather provider: {providers}] [city] [period] "
            "- Get weather forecast\n\n"
            "/mailing ([language code: {languages}] "
            "[weather provider: {providers}] [city] [period] [time: {times}] "
            "[mute: True (t,1) / False (f,0)]) "
            "- Sign up for or update the newsletter\n"
            "/unsubscribe_mailing - Unsubscribe from the newsletter\n\n"
            "Enjoy using!!!\n\n"
            "You can suggest an idea or report a bug by following the link: "
            "https://github.com/Gubchik123/WeatherGubchikBot/issues/new\n\n"
            "{bot_username} author contacts:\n"
            "CV site: https://hubariev.com\n"
            "LinkedIn: https://www.linkedin.com/in/nikita-hubariev\n"
            "Instagram: https://www.instagram.com/notwhale.1746\n\n"
            "Other projects of the author are available on:\n"
            "Project board: https://portfolio.hubariev.com\n"
            "GitHub: https://github.com/Gubchik123\n"
        ).format(
            bot_username=bot_me.username,
            languages=", ".join(LANGUAGES),
            providers=", ".join(WEATHER_PROVIDERS),
            times=", ".join(map(str, MAILING_TIMES)),
        )
    )
