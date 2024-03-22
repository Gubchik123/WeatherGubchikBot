from aiogram import Router

from .commands import commands_router


users_router = Router()

users_router.include_router(commands_router)
