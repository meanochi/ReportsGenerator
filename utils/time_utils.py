from datetime import datetime
import hashlib
import os
from config.rules import RULES

TIME_FORMAT = RULES.TIME_FORMAT

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
    seed_suffix = os.getenv("ATTENDANCE_VARIATION_SEED", "").strip()
    hash_input = f"{date_str}_{salt}_{seed_suffix}".encode("utf-8")
    hash_val = int(hashlib.md5(hash_input).hexdigest(), 16)
    # מחזיר מספר דקות בטווח של -DELTA_RANGE עד +DELTA_RANGE
    span = RULES.DELTA_RANGE_MINUTES
    return (hash_val % (2 * span + 1)) - span