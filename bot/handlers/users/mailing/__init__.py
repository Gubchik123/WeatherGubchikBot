from aiogram import Router

from .subscribe import router as subscribe_router
from .menu import handle_mailing_menu, router as menu_router
from .update import router as update_router
from .unsubscribe import router as unsubscribe_router


mailing_router = Router()

mailing_router.include_routers(
    subscribe_router, menu_router, update_router, unsubscribe_router
)
