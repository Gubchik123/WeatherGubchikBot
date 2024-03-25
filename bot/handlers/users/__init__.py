from aiogram import Router

from .commands import commands_router
from .menu import router as menu_router
from .profile import profile_router
from .weather import weather_router
from .mailing import mailing_router
from .other import router as other_router


users_router = Router()

users_router.include_routers(  # ! Order is important
    commands_router,
    menu_router,
    profile_router,
    mailing_router,
    weather_router,
    other_router,
)
