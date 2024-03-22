from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_bot_commands(bot: Bot) -> None:
    """Sets default bot commands for en, ua and ru languages."""
    bot_commands = {
        "uk": [
            BotCommand(command="start", description="Початок роботи з ботом"),
            BotCommand(
                command="help",
                description="Відображення основних правил використання",
            ),
            BotCommand(
                command="weather",
                description="Відображення інформації про погоду",
            ),
            BotCommand(
                command="goodbye", description="Завершення роботи з ботом"
            ),
        ],
        "en": [
            BotCommand(
                command="start", description="Start working with the bot"
            ),
            BotCommand(
                command="help", description="Display of basic usage rules"
            ),
            BotCommand(
                command="weather",
                description="Display information about the weather",
            ),
            BotCommand(
                command="goodbye", description="Ending work with the bot"
            ),
        ],
        "ru": [
            BotCommand(command="start", description="Начало работы з ботом"),
            BotCommand(
                command="help",
                description="Отображение основных правил использования",
            ),
            BotCommand(
                command="weather",
                description="Отображение информации о погоде",
            ),
            BotCommand(
                command="goodbye", description="Завершение работы с ботом"
            ),
        ],
    }

    for language_code, commands in bot_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
            language_code=language_code,
        )
