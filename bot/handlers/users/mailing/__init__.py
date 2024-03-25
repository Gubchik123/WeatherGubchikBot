from aiogram import Router

from .enable import router as enable_router
from .menu import router as menu_router


mailing_router = Router()

mailing_router.include_routers(enable_router, menu_router)
