from aiogram import Router

from .menu import router, handle_profile
from .language import router as language_router
from .timezone import router as timezone_router
from .weather_provider import router as weather_provider_router
from .search_history import router as search_history_router


profile_router = Router()

profile_router.include_routers(
    router,
    language_router,
    timezone_router,
    weather_provider_router,
    search_history_router,
)
