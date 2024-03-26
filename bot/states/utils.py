from typing import Union

from aiogram.fsm.context import FSMContext

from .mailing_setup import MailingSetup
from .weather_search import WeatherSearch
from .mailing_subscription import MailingSubscription


async def get_state_class_by_(
    fsm_context: FSMContext,
) -> Union[MailingSetup, WeatherSearch, MailingSubscription, None]:
    """Returns the state class by the given FSM context."""
    current_state = await fsm_context.get_state()

    if current_state:
        return {
            "WeatherSearch": WeatherSearch,
            "MailingSubscription": MailingSubscription,
        }.get(current_state.split(":")[0])
    return MailingSetup  # * because this one is always the first and the last state
