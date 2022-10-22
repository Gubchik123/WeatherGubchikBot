import re
from emoji import emojize
from constants import TEXT

DESC = ""
LANG = ""


def get_string_by_(regex: str):
    try:
        return re.search(regex, DESC)[0]
    except TypeError:
        return ''


def get_sun_description():
    return get_string_by_(
        regex={
            "uk": r'ясно,.+',
            "ru": r'ясно,.+',
            "en": r'clear,.+'
        }.get(LANG)
    )


def get_sun_behind_cloud_description():
    return get_string_by_(
        regex={
            "uk": r'.+(?:проясненнями|хмарність), без.+опадів',
            "ru": r'.+(?:прояснениями|облачность), без.+осадков',
            "en": r'.+(?:times|cloud), no.+precipitation'
        }.get(LANG)
    )


def get_cloud_description():
    return get_string_by_(
        regex={
            "uk": r'(?:похмуро|хмарно), без.+опадів',
            "ru": r'(?:пасмурно|облачно), без.+осадков',
            "en": r'(?:overcast|cloudy), no.+precipitation'
        }.get(LANG)
    )


def get_sun_behind_rain_cloud_description():
    return get_string_by_(
        regex={
            "uk": r'.+(проясненнями|хмарність),.+дощ',
            "ru": r'.+(прояснениями|облачность),.+дождь',
            "en": r'.+(times|cloud),.+rain'
        }.get(LANG)
    )


def get_cloud_with_rain_description():
    return get_string_by_(
        regex={
            "uk": r'(?:похмуро|хмарно),.+дощ',
            "ru": r'(?:пасмурно|облачно),.+дождь',
            "en": r'(?:overcast|cloudy),.+rain'
        }.get(LANG)
    )


def get_weather_emoji_by_(desc: str):
    """Function for returning weather emoji by description"""
    global DESC, LANG

    desc = desc.lower()
    DESC = desc
    LANG = TEXT().lang_code

    return {
        get_sun_description():
            emojize(":sun:"),  # ☀️
        get_sun_behind_cloud_description():
            emojize(":sun_behind_cloud:"),  # ⛅️
        get_cloud_description():
            emojize(":cloud:"),  # ☁️
        get_sun_behind_rain_cloud_description():
            emojize(":sun_behind_rain_cloud:"),  # 🌦
        get_cloud_with_rain_description():
            emojize(":cloud_with_rain:")  # 🌧
    }.get(desc, '')


def get_moon_emoji_by_(desc: str):
    return {
        "повня":
            emojize(":full_moon:"),  # 🌕
        "спадаючий опуклий місяць":
            emojize(":waning_gibbous_moon:"),  # 🌖
        "остання чверть":
            emojize(":last_quarter_moon:"),  # 🌗
        "спадаючий півмісяць":
            emojize(":waning_crescent_moon:"),  # 🌘
        "новий місяць":
            emojize(":new_moon:"),  # 🌑
        "зростаючий півмісяць":
            emojize(":waxing_crescent_moon:"),  # 🌒
        "перша чверть":
            emojize(":first_quarter_moon:"),  # 🌓
        "зростаючий опуклий місяць":
            emojize(":waxing_gibbous_moon:")  # 🌔
    }.get(desc.lower(), '')
