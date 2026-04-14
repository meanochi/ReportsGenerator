from datetime import datetime, timedelta
import hashlib

TIME_FORMAT = "%H:%M"

def str_to_time(time_str: str) -> datetime:
    """Converts a time string to a datetime object (using a dummy date)."""
    return datetime.strptime(time_str, TIME_FORMAT)

def time_to_str(dt: datetime) -> str:
    """Converts a datetime object back to a time string."""
    return dt.strftime(TIME_FORMAT)

def get_deterministic_delta(date_str: str, salt: str = "start") -> int:
    """
    Generates a deterministic number of minutes to add/subtract 
    based on the date string and a salt.
    """
    hash_input = f"{date_str}_{salt}".encode('utf-8')
    hash_val = int(hashlib.md5(hash_input).hexdigest(), 16)
    # מחזיר מספר דקות בטווח של -15 עד +15 
    return (hash_val % 31) - 15