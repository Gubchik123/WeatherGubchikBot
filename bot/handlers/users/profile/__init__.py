from aiogram import Router

from .profile import router, handle_profile
from .language import router as language_router
from .timezone import router as timezone_router


profile_router = Router()

profile_router.include_routers(router, language_router, timezone_router)
