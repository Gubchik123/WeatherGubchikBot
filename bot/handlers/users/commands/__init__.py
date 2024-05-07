from aiogram import Router

from .start import router as start_command_router
from .help import router as help_command_router
from .menu import router as menu_command_router
from .weather import router as weather_command_router
from .moon import router as moon_command_router
from .profile import router as profile_command_router
from .mailing import router as mailing_command_router
from .goodbye import router as goodbye_command_router


commands_router = Router()

commands_router.include_routers(
    start_command_router,
    help_command_router,
    menu_command_router,
    weather_command_router,
    moon_command_router,
    profile_command_router,
    mailing_command_router,
    goodbye_command_router,
)
