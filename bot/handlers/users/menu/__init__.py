from aiogram import Router

from .menu import menu, router
from .language import router as language_router
from .timezone import router as timezone_router


menu_router = Router()

menu_router.include_routers(router, language_router, timezone_router)
