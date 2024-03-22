from aiogram import Router

from .city import router as city_router
from .city_title import router as city_title_router
from .period import router as period_router


weather_router = Router()

weather_router.include_routers(city_router, city_title_router, period_router)
