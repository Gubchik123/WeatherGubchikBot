from aiogram import Router

from .menu import router as menu_router


mailing_router = Router()

mailing_router.include_router(menu_router)
