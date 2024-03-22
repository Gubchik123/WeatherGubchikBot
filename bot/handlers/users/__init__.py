from aiogram import Router

from .commands import commands_router
from .menu import menu_router
from .weather import weather_router


users_router = Router()

users_router.include_routers(
    commands_router,
    menu_router,
    weather_router,
)
