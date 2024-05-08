from aiogram import Router

from .admins import admins_router
from .users import users_router
from .channels import channels_router


handlers_router = Router()

handlers_router.include_routers(channels_router, admins_router, users_router)
