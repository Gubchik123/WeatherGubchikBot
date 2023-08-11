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


def check_sun_description() -> str:
    """For getting ☀️ emoji description by RegExp and language"""
    string = get_string_by_(
        regex={"ua": r"ясно,.+", "ru": r"ясно,.+", "en": r"clear,.+"}.get(LANG)
    )
    return (
        emojize(":sun:")
        if string == DESC
        else check_sun_behind_cloud_description()
    )


def check_sun_behind_cloud_description() -> str:
    """For getting ⛅️ emoji description by RegExp and language"""
    string = get_string_by_(
        regex={
            "ua": r".+(?:проясненнями|хмарність), без.+опадів",
            "ru": r".+(?:прояснениями|облачность), без.+осадков",
            "en": r".+(?:times|cloud), no.+precipitation",
        }.get(LANG)
    )
    return (
        emojize(":sun_behind_cloud:")
        if string == DESC
        else check_cloud_description()
    )


def check_cloud_description() -> str:
    """For getting ☁️ emoji description by RegExp and language"""
    string = get_string_by_(
        regex={
            "ua": r"(?:похмуро|хмарно), без.+опадів",
            "ru": r"(?:пасмурно|облачно), без.+осадков",
            "en": r"(?:overcast|cloudy), no.+precipitation",
        }.get(LANG)
    )
    return (
        emojize(":cloud:")
        if string == DESC
        else check_sun_behind_rain_cloud_description()
    )


def check_sun_behind_rain_cloud_description() -> str:
    """For getting 🌦 emoji description by RegExp and language"""
    string = get_string_by_(
        regex={
            "ua": r".+(проясненнями|хмарність),.+дощ",
            "ru": r".+(прояснениями|облачность),.+дождь",
            "en": r".+(times|cloud),.+rain",
        }.get(LANG)
    )
    return (
        emojize(":sun_behind_rain_cloud:")
        if string == DESC
        else check_cloud_with_rain_description()
    )


def check_cloud_with_rain_description() -> str:
    """For getting 🌧 emoji description by RegExp and language"""
    string = get_string_by_(
        regex={
            "ua": r"(?:похмуро|хмарно),.+(?:дощ|опади)",
            "ru": r"(?:пасмурно|облачно),.+(?:дождь|осадки)",
            "en": r"(?:overcast|cloudy),.+(?:rain|precipitation)",
        }.get(LANG)
    )
    return (
        emojize(":cloud_with_rain:")
        if string == DESC
        else check_cloud_with_lightning_description()
    )


def check_cloud_with_lightning_description() -> str:
    """For getting 🌩 emoji description by RegEcp and language"""
    string = get_string_by_(
        regex={
            "ua": r".+(?:гроза|блискавиці).+",
            "ru": r".+(?:гроза|молнии).+",
            "en": r".+(?:thunderstorm|lightning).+",
        }.get(LANG)
    )
    return (
        emojize(":cloud_with_lightning:")
        if string == DESC
        else check_cloud_with_lightning_and_rain_description()
    )


def check_cloud_with_lightning_and_rain_description() -> str:
    """For getting ⛈ emoji description by RegExp and language"""
    string = get_string_by_(
        regex={
            "ua": r"(?:гроз).+,.+(?:дощ|опади)",
            "ru": r"(?:гроз).+,.+(?:дождь|осадки)",
            "en": r"(?:thunder|storm).+,.+(?:rain|precipitation)",
        }.get(LANG)
    )
    return (
        emojize(":cloud_with_lightning_and_rain:")
        if string == DESC
        else check_cloud_with_snow_description()
    )


def check_cloud_with_snow_description() -> str:
    """For getting 🌨️ emoji description by RegExp and language"""
    string = get_string_by_(
        regex={"ua": r".*сніг.*", "ru": r".*снег.*", "en": r".*snow.*"}.get(
            LANG
        )
    )
    return emojize(":cloud_with_snow:") if string == DESC else ""


def get_weather_emoji_by_(desc: str) -> str:
    """For getting weather emoji by description and language"""
    global DESC, LANG

    desc = desc.lower()
    DESC = desc
    LANG = TEXT().lang_code

    return check_sun_description()
