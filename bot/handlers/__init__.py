from aiogram import Router

from .admins import admins_router
from .users import users_router
from .channels import channels_router
from .inline import inline_router


handlers_router = Router()

handlers_router.include_routers(
    inline_router, channels_router, admins_router, users_router
)
