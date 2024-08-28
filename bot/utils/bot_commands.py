from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
)


async def set_default_commands_for_(bot: Bot) -> None:
    """Sets default bot commands for en, ua and ru languages."""
    await _set_private_chats_commands_for_(bot)
    await _set_group_chats_commands_for_(bot)


START_COMMAND = {
    "uk": BotCommand(command="start", description="Початок роботи з ботом"),
    "en": BotCommand(
        command="start", description="Start working with the bot"
    ),
    "ru": BotCommand(command="start", description="Начало работы с ботом"),
}

HELP_COMMAND = {
    "uk": BotCommand(
        command="help", description="Отримати основні правила використання"
    ),
    "en": BotCommand(command="help", description="Get basic usage rules"),
    "ru": BotCommand(
        command="help", description="Получить основные правила использования"
    ),
}

MOON_COMMAND = {
    "uk": BotCommand(command="moon", description="Отримати фазу місяця"),
    "en": BotCommand(command="moon", description="Get moon phase"),
    "ru": BotCommand(command="moon", description="Получить фазу луны"),
}

WEATHER_COMMAND = {
    "uk": BotCommand(command="weather", description="Отримати прогноз погоди"),
    "en": BotCommand(command="weather", description="Get weather forecast"),
    "ru": BotCommand(command="weather", description="Получить прогноз погоды"),
}


async def _set_private_chats_commands_for_(bot: Bot):
    """Sets default bot commands for private chats."""
    bot_commands = {
        "uk": [
            BotCommand(command="start", description="Початок роботи з ботом"),
            HELP_COMMAND["uk"],
            BotCommand(command="menu", description="Отримати головне меню"),
            MOON_COMMAND["uk"],
            WEATHER_COMMAND["uk"],
            BotCommand(
                command="profile", description="Отримати профіль користувача"
            ),
            BotCommand(
                command="mailing",
                description="Отримати меню розсилки / Підписатися або оновити розсилку",
            ),
            BotCommand(
                command="goodbye", description="Призупинити роботу з ботом"
            ),
        ],
        "en": [
            BotCommand(
                command="start", description="Start working with the bot"
            ),
            HELP_COMMAND["en"],
            BotCommand(command="menu", description="Get main menu"),
            MOON_COMMAND["en"],
            WEATHER_COMMAND["en"],
            BotCommand(command="profile", description="Get user profile"),
            BotCommand(
                command="mailing",
                description="Get mailing menu / Sign up for or update the newsletter",
            ),
            BotCommand(
                command="goodbye", description="Pause working with the bot"
            ),
        ],
        "ru": [
            BotCommand(command="start", description="Начало работы с ботом"),
            HELP_COMMAND["ru"],
            BotCommand(command="menu", description="Получить главное меню"),
            MOON_COMMAND["ru"],
            WEATHER_COMMAND["ru"],
            BotCommand(
                command="profile", description="Получить профиль пользователя"
            ),
            BotCommand(
                command="mailing",
                description="Получить меню рассылки / Подписаться на рассылку или обновить ее",
            ),
            BotCommand(
                command="goodbye", description="Приостановить работу с ботом"
            ),
        ],
    }
    for language_code, commands in bot_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeAllPrivateChats(),
            language_code=language_code,
        )


async def _set_group_chats_commands_for_(bot: Bot):
    """Sets default bot commands for group chats."""
    bot_commands = {
        "uk": [
            HELP_COMMAND["uk"],
            MOON_COMMAND["uk"],
            WEATHER_COMMAND["uk"],
            BotCommand(
                command="mailing",
                description="Підписатися або оновити розсилку",
            ),
            BotCommand(
                command="unsubscribe_mailing ",
                description="Відписатися від розсилки",
            ),
        ],
        "en": [
            HELP_COMMAND["en"],
            MOON_COMMAND["en"],
            WEATHER_COMMAND["en"],
            BotCommand(
                command="mailing",
                description="Sign up for or update the newsletter",
            ),
            BotCommand(
                command="unsubscribe_mailing ",
                description="Unsubscribe from the newsletter",
            ),
        ],
        "ru": [
            HELP_COMMAND["ru"],
            MOON_COMMAND["ru"],
            WEATHER_COMMAND["ru"],
            BotCommand(
                command="mailing",
                description="Подписаться на рассылку или обновить ее",
            ),
            BotCommand(
                command="unsubscribe_mailing ",
                description="Отписаться от рассылки",
            ),
        ],
    }
    for language_code, commands in bot_commands.items():
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeAllGroupChats(),
            language_code=language_code,
        )
