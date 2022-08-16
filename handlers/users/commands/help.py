from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from bot_info import DP
from handlers.users.menu import menu


@DP.message_handler(CommandHelp())
async def command_help(message: types.Message):
    await message.answer("Команди:\n"
                         "/start   - для запуску\перезапуску бота\n"
                         "/help    - для ознайомлення зі справкою\n"
                         "/weather - для перегляду прогнозу погоди\n"
                         "/moon    - для перегляду фази місяця\n"
                         "/goodbye - для завершення спілкування\n\n"

                         "Оформіть розсилку, щоб кожного для о 09:00 дізнаватися " 
                         "про погоду в місті, яке ви обирете (в будь-який час її " 
                         "можно відключити)\n\n"

                         "Раджу використати кнопки для задуманого результату\n\n"

                         "Приємного використання!!!")
    await menu(message)
