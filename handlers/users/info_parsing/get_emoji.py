import re
from emoji import emojize

DESC = ""


def get_string_by_(regex: str):
    try:
        return re.search(regex, DESC)[0]
    except TypeError:
        return ''


def get_weather_emoji_by_(desc: str):
    """Function for returning weather emoji by description"""
    global DESC

    desc = desc.lower()
    DESC = desc

    sun_behind_cloud_description = get_string_by_(
        regex=r'.+(?:проясненнями|хмарність), без.+опадів'
    )
    cloud_description = get_string_by_(
        regex=r'(?:похмуро|хмарно), без.+опадів'
    )
    sun_behind_rain_cloud_description = get_string_by_(
        regex=r'.+, невеликий дощ'
    )
    cloud_with_rain_description = get_string_by_(
        regex=r'.+, дощ'
    )

    return {
        "ясно, без опадів":                emojize(":sun:"),
        sun_behind_cloud_description:      emojize(":sun_behind_cloud:"),
        cloud_description:                 emojize(":cloud:"),
        sun_behind_rain_cloud_description: emojize(":sun_behind_rain_cloud:"),
        cloud_with_rain_description:       emojize(":cloud_with_rain:")
    }.get(desc, '')
