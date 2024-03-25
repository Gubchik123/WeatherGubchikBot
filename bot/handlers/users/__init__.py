from aiogram import Router

from .commands import commands_router
from .profile import profile_router
from .weather import weather_router


users_router = Router()

users_router.include_routers(
    commands_router,
    profile_router,
    weather_router,
)
