from datetime import datetime
import pytz


def convert_utc_to_jst(utc_dt) -> datetime:
    return utc_dt.astimezone(pytz.timezone('Asia/Tokyo'))


def datetime_to_str(dt: datetime, format_str: str) -> str:
    return dt.strftime(format_str)


def str_to_datetime(dt_str: str, format_str: str) -> datetime:
    return datetime.strptime(dt_str, format_str)