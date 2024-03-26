from aiogram import Router

from .mute import router as mute_router
from .time import router as time_router
from .period import router as period_router
from .city import router as city_router


update_router = Router()

update_router.include_routers(
    mute_router, time_router, period_router, city_router
)
