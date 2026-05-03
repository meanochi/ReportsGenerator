"""Configuration and business rules for attendance report modifications."""
from dataclasses import dataclass

@dataclass(frozen=True)
class RulesPerVariant:
    """Business rules that apply to all report variants."""
    MAX_WORK_HOURS: int = 12
    MIN_WORK_HOURS: int = 1
    MAX_BREAK_MINUTES: int = 120
    DELTA_RANGE_MINUTES: int = 15
    TIME_FORMAT: str = "%H:%M"

@dataclass(frozen=True)
class TypeAReportRules:
    """Rules specific to Type A reports."""
    COLUMNS: tuple = ("Date", "Day", "Location", "Entry", "Exit", "Break", "Total Hours", "Base 100%", "Overtime 125%", "Overtime 150%")

@dataclass(frozen=True)
class TypeBReportRules:
    """Rules specific to Type B reports."""
    COLUMNS: tuple = ("Date", "Day", "Entry Time", "Exit Time", "Total Hours", "Notes")

RULES = RulesPerVariant()
TYPE_A_RULES = TypeAReportRules()
TYPE_B_RULES = TypeBReportRules()
