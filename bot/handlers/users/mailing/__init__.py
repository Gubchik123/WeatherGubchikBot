from aiogram import Router

from .enable import router as enable_router
from .menu import handle_mailing_menu, router as menu_router


mailing_router = Router()

mailing_router.include_routers(enable_router, menu_router)
