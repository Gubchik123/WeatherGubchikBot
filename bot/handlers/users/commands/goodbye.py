from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from utils.decorators import before_handler_clear_state
from keyboards.default.maker import make_keyboard, make_button


router = Router()


@router.message(Command("goodbye"))
@router.message(F.text.lower() == __("end communication"))
@before_handler_clear_state
async def handle_goodbye_command(message: Message, *args):
    """Handles the /goodbye command."""
    await message.answer_sticker(
        "CAACAgIAAxkBAAICBGLIifDJ3jPz291sEcRKE5EO4j99AALsAwAC0lqIAZ0zny94Yp4oKQQ"
    )
    await message.answer(
        _(
            "Bye, {name}, come bake again!\nNext time just type or press /start"
        ).format(name=message.from_user.first_name),
        reply_markup=make_keyboard([[make_button("/start")]], one_time=True),
    )
