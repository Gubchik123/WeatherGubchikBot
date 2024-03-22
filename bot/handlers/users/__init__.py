from aiogram import Router

from .menu import menu_router
from .commands import commands_router


users_router = Router()

users_router.include_routers(menu_router, commands_router)
