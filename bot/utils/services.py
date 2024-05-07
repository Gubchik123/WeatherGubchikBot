def get_city_from_(event_data: str) -> str:
    """Returns city from the given event data."""
    city = event_data.split(":")[-1].strip().lower()
    city = city.split("(")[0].strip()
    return _strip_emoji_from_(city)


def _strip_emoji_from_(city: str) -> str:
    """Returns city without emoji at the beginning if it is there."""
    emoji_ranges = (("\U0001F1E0", "\U0001F1FF"),)  # flags
    while city and any(start <= city[0] <= end for start, end in emoji_ranges):
        city = city[1:]
    return city.strip()
