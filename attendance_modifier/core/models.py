from dataclasses import dataclass, field
from typing import List, Optional
from core.enums import ReportType

@dataclass
class AttendanceRow:
    """DTO representing a single row in the attendance report."""
    date: str
    original_in: str
    original_out: str
    raw_text_line: str
    new_in: Optional[str] = None
    new_out: Optional[str] = None

@dataclass
class AttendanceReport:
    """DTO representing the entire parsed report."""
    report_type: ReportType
    employee_name: str = "Unknown"
    employee_id: str = "Unknown"
    rows: List[AttendanceRow] = field(default_factory=list)
    raw_text: str = ""