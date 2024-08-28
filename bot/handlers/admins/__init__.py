from aiogram import Router

from .users import router as users_router
from .channels import router as channels_router
from .mailing import router as mailing_router
from .search_logs import router as search_logs_router
from .scheduler import router as scheduler_router


admins_router = Router()

admins_router.include_routers(
    users_router,
    channels_router,
    mailing_router,
    search_logs_router,
    scheduler_router,
)
