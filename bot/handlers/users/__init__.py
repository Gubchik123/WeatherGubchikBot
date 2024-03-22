from aiogram import Router

from .commands import commands_router
from .menu import router as menu_router
from .timezone import router as timezone_router


users_router = Router()

users_router.include_routers(commands_router, menu_router, timezone_router)
