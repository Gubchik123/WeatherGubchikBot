from aiogram.types import BotCommand, BotCommandScopeDefault
from bot_info import BOT


async def set_default_commands(message) -> None:
    """For setting default bot commands for 3 language"""
    bot_commands = {
        "uk": [
            BotCommand("start", "Початок роботи з ботом"),
            BotCommand("language", "Змінення мови бота"),
            BotCommand("help", "Відображення основних правил використання"),
            BotCommand("weather", "Відображення інформації про погоду"),
            BotCommand("goodbye", "Завершення роботи з ботом"),
        ],
        "en": [
            BotCommand("start", "Start working with the bot"),
            BotCommand("language", "Change the language of the bot"),
            BotCommand("help", "Display of basic usage rules"),
            BotCommand("weather", "Display information about the weather"),
            BotCommand("goodbye", "Ending work with the bot"),
        ],
        "ru": [
            BotCommand("start", "Начало работы з ботом"),
            BotCommand("language", "Изменения языка бота"),
            BotCommand("help", "Отображение основных правил использования"),
            BotCommand("weather", "Отображение информауии о погоде"),
            BotCommand("goodbye", "Завершение работы с ботом"),
        ],
    }

    for language_code, commands in bot_commands.items():
        await BOT.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
            language_code=language_code,
        )
