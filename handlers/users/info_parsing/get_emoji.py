from emoji import emojize


def get_weather_emoji_by_(desc: str):
    """Function for returning weather emoji by description"""
    sun_behind_cloud_description = [
        "мінлива хмарність, без опадів", "невелика хмарність, без опадів",
        "хмарно з проясненнями, без опадів", "хмарно з проясненнями, без істот. опадів",
        "невелика хмарність, без істот. опадів", "мінлива хмарність, без істот. опадів"
    ]

    cloud_description = [
        "похмуро, без опадів", "хмарно, без опадів",
        "похмуро, без істот. опадів", "хмарно, без істот. опадів"
    ]

    sun_behind_rain_cloud_description = [
        "похмуро, невеликий дощ", "мінлива хмарність, невеликий дощ",
        "хмарно з проясненнями, невеликий дощ", "невелика хмарність, невеликий дощ"
    ]

    cloud_with_rain_description = [
        "хмарно, дощ", "похмуро, дощ", "хмарно, невеликий дощ"
    ]

    desc = desc.lower()

    if "ясно" in desc:
        return emojize(":sun:")
    elif desc in sun_behind_cloud_description:
        return emojize(":sun_behind_cloud:")
    elif desc in cloud_description:
        return emojize(":cloud:")
    elif desc in sun_behind_rain_cloud_description:
        return emojize(":sun_behind_rain_cloud:")
    elif desc in cloud_with_rain_description:
        return emojize(":cloud_with_rain:")
    else:
        return ''
