from typing import Union

from aiogram.fsm.context import FSMContext

from .mailing_setup import MailingSetup
from .weather_search import WeatherSearch


async def get_state_class_by_(
    fsm_context: FSMContext,
) -> Union[WeatherSearch, MailingSetup, None]:
    """Returns the state class by the given FSM context."""
    current_state = await fsm_context.get_state()

    if current_state:
        return {
            "MailingSetup": MailingSetup,
            "WeatherSearch": WeatherSearch,
        }.get(current_state.split(":")[0])
    return None
