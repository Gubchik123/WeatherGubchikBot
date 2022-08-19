from aiogram.types import BotCommand, BotCommandScopeDefault

from bot_info import BOT


async def set_default_commands(message):
    bot_commands = {
        "en": [
            BotCommand("start",   "Start of working with bot"),
            BotCommand("help",    "General rules for using"),
            BotCommand("weather", "Showing information about the weather"),
            BotCommand("moon",    "Showing information about moon phase"),
            BotCommand("goodbye", "Finish of working with bot")
        ],
        "uk": [
            BotCommand("start",   "Початок роботи з ботом"),
            BotCommand("help",    "Основні правила використання"),
            BotCommand("weather", "Відображення інформації про погоду"),
            BotCommand("moon",    "Відображення інформації про фазу місяця"),
            BotCommand("goodbye", "Кінець роботи з ботом")
        ],
        "ru": [
            BotCommand("start",   "Начало работы с ботом"),
            BotCommand("help",    "Основные правила использования"),
            BotCommand("weather", "Отображение информации о погоде"),
            BotCommand("moon",    "Отображение информации о фазе луны"),
            BotCommand("goodbye", "Конец работы с ботом")
        ],
    }

    for language_code, commands in bot_commands.items():
        await BOT.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
            language_code=language_code
        )
