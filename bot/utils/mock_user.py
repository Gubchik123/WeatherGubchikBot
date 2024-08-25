from typing import NamedTuple


class MockUser(NamedTuple):
    """Represents a mock telegram user."""

    id: int  # instead of chat_id
    username: str
    full_name: str
