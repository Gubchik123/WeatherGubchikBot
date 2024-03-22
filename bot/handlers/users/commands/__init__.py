from aiogram import Router

from .start import router as start_command_router


commands_router = Router()


commands_router.include_router(start_command_router)
