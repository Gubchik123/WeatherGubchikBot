from googletrans import Translator
from aiogram.types import BotCommand, BotCommandScopeDefault

from bot_info import BOT


async def set_default_commands(message):
    translator = Translator()

    uk_commands = {
        "start":    "Початок роботи з ботом",
        "language": "Змінення мови бота",
        "help":     "Відображення основних правил використання",
        "weather":  "Відображення інформації про погоду",
        "moon":     "Відображення інформації про фазу місяця",
        "goodbye":  "Завершення роботи з ботом"
    }

    bot_commands: dict = {}

    for lang_code in ("uk", "en", "ru"):
        commands: list = []

        for command, text in uk_commands.items():
            if lang_code != "uk":
                text = translator.translate(text, dest=lang_code).text

            commands.append(
                BotCommand(command, text)
            )

        bot_commands[lang_code] = commands

    for language_code, commands in bot_commands.items():
        await BOT.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
            language_code=language_code
        )
