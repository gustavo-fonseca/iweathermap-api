from datetime import datetime
import pytz


def strptime_utc_to_tz(date_string, format_string, tz_string):
    """Implements a localized datetime.strptime

    Args:
        date_string (str): e.g. "2020-12-20 09:20:00"
        format_string (str): e.g. "%Y-%m-%d %H:%M:%S"
        tz_string (str): e.g. "America/Sao_Paulo"

    Returns:
        datetime: Localized datetime instance

    """
    dt = datetime.strptime(date_string, format_string)

    # setting up timezone
    dt_utc = pytz.utc.localize(dt)
    dt_tz = dt_utc.astimezone(pytz.timezone(tz_string))
    return dt_tz
