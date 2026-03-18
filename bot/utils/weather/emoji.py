import re

from aiogram.utils.i18n import gettext as _


def get_moon_emoji_by_(description: str) -> str:
    """Returns moon emoji by the given description."""
    return {
        _("Full Moon").lower(): "🌕",
        _("Waning Gibbous").lower(): "🌖",
        _("Third Quarter").lower(): "🌗",
        _("Waning Crescent").lower(): "🌘",
        _("New Moon").lower(): "🌑",
        _("Waxing Crescent").lower(): "🌒",
        _("First Quarter").lower(): "🌓",
        _("Waxing Gibbous").lower(): "🌔",
    }.get(description.lower(), "")


def get_weather_emoji_by_(description: str, lang_code: str) -> str:
    """Returns weather by the given description and language code."""
    return _check_sun_(description.lower(), lang_code)


def _get_string_by_(regex: str, description: str) -> str:
    """Returns string by the given RegExp and description
    if it's correct else empty string."""
    try:
        return re.search(regex, description)[0]
    except TypeError:
        return ""


def _check_sun_(description: str, lang_code: str) -> str:
    """Checks the ☀️ by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r"ясно.*",
            "ru": r"(?:ясно|безоблачно).*",
            "en": r"(?:clear|fair).*",
        }.get(lang_code),
        description,
    )
    return (
        "☀️"
        if string == description
        else _check_sun_behind_cloud_(description, lang_code)
    )


def _check_sun_behind_cloud_(description: str, lang_code: str) -> str:
    """Checks the ⛅️ by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r".*(?:проясненнями|хмарність), без.+опадів",
            "ru": r".*(?:прояснениями|облачность), без.+осадков",
            "en": r".*(?:times|cloud), no.+precipitation",
        }.get(lang_code),
        description,
    )
    return (
        "⛅️"
        if string == description
        else _check_cloud_(description, lang_code)
    )


def _check_cloud_(description: str, lang_code: str) -> str:
    """Checks the ☁️ by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r".*(?:похмуро|хмарно), без.+опадів",
            "ru": r".*(?:пасмурно|облачно), без.+осадков",
            "en": r".*(?:overcast|cloudy), no.+precipitation",
        }.get(lang_code),
        description,
    )
    return (
        "☁️"
        if string == description
        else _check_sun_behind_rain_cloud_(description, lang_code)
    )


def _check_sun_behind_rain_cloud_(description: str, lang_code: str) -> str:
    """Checks the 🌦 by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r".*(проясненнями|хмарність),.+дощ",
            "ru": r".*(прояснениями|облачность),.+дождь",
            "en": r".*(times|cloud),.+rain",
        }.get(lang_code),
        description,
    )
    return (
        "🌦"
        if string == description
        else _check_cloud_with_rain_(description, lang_code)
    )


def _check_cloud_with_rain_(description: str, lang_code: str) -> str:
    """Checks the 🌧 by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r".*(?:похмуро|хмарно),.+(?:дощ|опади)",
            "ru": r".*(?:пасмурно|облачно),.+(?:дождь|осадки)",
            "en": r".*(?:overcast|cloudy),.+(?:rain|precipitation)",
        }.get(lang_code),
        description,
    )
    return (
        "🌧"
        if string == description
        else _check_cloud_with_lightning_(description, lang_code)
    )


def _check_cloud_with_lightning_(description: str, lang_code: str) -> str:
    """Checks the 🌩 by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r".+(?:гроза|блискавиці).+",
            "ru": r".+(?:гроза|молнии).+",
            "en": r".+(?:thunderstorm|lightning).+",
        }.get(lang_code),
        description,
    )
    return (
        "🌩"
        if string == description
        else _check_cloud_with_lightning_and_rain_(description, lang_code)
    )


def _check_cloud_with_lightning_and_rain_(
    description: str, lang_code: str
) -> str:
    """Checks the ⛈ by the given description and language code."""
    string = _get_string_by_(
        {
            "ua": r"(?:гроз).+,.+(?:дощ|опади)",
            "ru": r"(?:гроз).+,.+(?:дождь|осадки)",
            "en": r"(?:thunder|storm).+,.+(?:rain|precipitation)",
        }.get(lang_code),
        description,
    )
    return (
        "⛈"
        if string == description
        else _check_cloud_with_snow_(description, lang_code)
    )


def _check_cloud_with_snow_(description: str, lang_code: str) -> str:
    """Checks the 🌨️ by the given description and language code."""
    string = _get_string_by_(
        {"ua": r".*сніг.*", "ru": r".*снег.*", "en": r".*snow.*"}.get(
            lang_code
        ),
        description,
    )
    return "🌨️" if string == description else ""
