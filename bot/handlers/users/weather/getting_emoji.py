import re
from emoji import emojize
from constants import TEXT

DESC = ""
LANG = ""


def get_string_by_(regex: str) -> str:
    """For getting string by RegExp if it is correct else empty string"""
    try:
        return re.search(regex, DESC)[0]
    except TypeError:
        return ""


def get_sun_description() -> str:
    """For getting ☀️ emoji description by RegExp and language"""
    return get_string_by_(
        regex={"uk": r"ясно,.+", "ru": r"ясно,.+", "en": r"clear,.+"}.get(LANG)
    )


def get_sun_behind_cloud_description() -> str:
    """For getting ⛅️ emoji description by RegExp and language"""
    return get_string_by_(
        regex={
            "uk": r".+(?:проясненнями|хмарність), без.+опадів",
            "ru": r".+(?:прояснениями|облачность), без.+осадков",
            "en": r".+(?:times|cloud), no.+precipitation",
        }.get(LANG)
    )


def get_cloud_description() -> str:
    """For getting ☁️ emoji description by RegExp and language"""
    return get_string_by_(
        regex={
            "uk": r"(?:похмуро|хмарно), без.+опадів",
            "ru": r"(?:пасмурно|облачно), без.+осадков",
            "en": r"(?:overcast|cloudy), no.+precipitation",
        }.get(LANG)
    )


def get_sun_behind_rain_cloud_description() -> str:
    """For getting 🌦 emoji description by RegExp and language"""
    return get_string_by_(
        regex={
            "uk": r".+(проясненнями|хмарність),.+дощ",
            "ru": r".+(прояснениями|облачность),.+дождь",
            "en": r".+(times|cloud),.+rain",
        }.get(LANG)
    )


def get_cloud_with_rain_description() -> str:
    """For getting 🌧 emoji description by RegExp and language"""
    return get_string_by_(
        regex={
            "uk": r"(?:похмуро|хмарно),.+(?:дощ|опади)",
            "ru": r"(?:пасмурно|облачно),.+(?:дождь|осадки)",
            "en": r"(?:overcast|cloudy),.+(?:rain|precipitation)",
        }.get(LANG)
    )


def get_cloud_with_snow_description() -> str:
    """For getting 🌨️ emoji description by RegExp and language"""
    return get_string_by_(
        regex={"uk": r".*сніг.*", "ru": r".*снег.*", "en": r".*snow.*"}.get(LANG)
    )


def get_weather_emoji_by_(desc: str) -> str:
    """For getting weather emoji by description and language"""
    global DESC, LANG

    desc = desc.lower()
    DESC = desc
    LANG = TEXT().lang_code

    return {
        get_sun_description(): emojize(":sun:"),  # ☀️
        get_sun_behind_cloud_description(): emojize(":sun_behind_cloud:"),  # ⛅️
        get_cloud_description(): emojize(":cloud:"),  # ☁️
        get_sun_behind_rain_cloud_description(): emojize(
            ":sun_behind_rain_cloud:"
        ),  # 🌦
        get_cloud_with_rain_description(): emojize(":cloud_with_rain:"),  # 🌧
        get_cloud_with_snow_description(): emojize(":cloud_with_snow:"),  # 🌨️
    }.get(desc, "")
