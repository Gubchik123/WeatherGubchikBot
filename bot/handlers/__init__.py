from aiogram import Router

from .admins import admins_router
from .users import users_router


handlers_router = Router()

handlers_router.include_routers(admins_router, users_router)
