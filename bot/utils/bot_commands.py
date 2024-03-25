from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_default_bot_commands(bot: Bot) -> None:
    """Sets default bot commands for en, ua and ru languages."""
    bot_commands = {
        "uk": [
            BotCommand(command="start", description="Початок роботи з ботом"),
            BotCommand(
                command="help",
                description="Отримати основні правила використання",
            ),
            BotCommand(
                command="weather", description="Отримати прогноз погоди"
            ),
            BotCommand(
                command="profile", description="Отримати профіль користувача"
            ),
            BotCommand(
                command="mailing",
                description="Отримати меню розсилки / Підписатися на розсилку",
            ),
            BotCommand(
                command="goodbye", description="Призупинити роботу з ботом"
            ),
        ],
        "en": [
            BotCommand(
                command="start", description="Start working with the bot"
            ),
            BotCommand(command="help", description="Get basic usage rules"),
            BotCommand(command="weather", description="Get weather forecast"),
            BotCommand(command="profile", description="Get user profile"),
            BotCommand(
                command="mailing",
                description="Get mailing menu / Sign up for the newsletter",
            ),
            BotCommand(
                command="goodbye", description="Pause working with the bot"
            ),
        ],
        "ru": [
            BotCommand(command="start", description="Начало работы с ботом"),
            BotCommand(
                command="help",
                description="Получить основные правила использования",
            ),
            BotCommand(
                command="weather", description="Получить прогноз погоды"
            ),
            BotCommand(
                command="profile", description="Получить профиль пользователя"
            ),
            BotCommand(
                command="mailing",
                description="Получить меню рассылки / Подписаться на рассылку",
            ),
            BotCommand(
                command="goodbye", description="Приостановить работу с ботом"
            ),
        ],
    }

    for language_code, commands in bot_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeDefault(),
            language_code=language_code,
        )
