from aiogram import Router

from .start import router as start_command_router
from .help import router as help_command_router


commands_router = Router()


commands_router.include_routers(start_command_router, help_command_router)
