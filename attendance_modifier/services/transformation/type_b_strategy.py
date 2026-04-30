import dataclasses
from datetime import timedelta
from core.models import AttendanceRow
from utils.time_utils import str_to_time, time_to_str, get_deterministic_delta
from services.transformation.base_strategy import BaseTransformationStrategy

_BREAK_MINUTES = 30
_STANDARD_HOURS = 8.0


class TypeBTransformationStrategy(BaseTransformationStrategy):
    """
    Complex strategy for Type B (employee card) reports.
    Deducts a fixed break and calculates 125% overtime beyond 8 hours.
    """

    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        if not row.original_in or not row.original_out:
            return row

        new_in = str_to_time(row.original_in) + timedelta(
            minutes=get_deterministic_delta(row.date, salt="in")
        )
        new_out = str_to_time(row.original_out) + timedelta(
            minutes=get_deterministic_delta(row.date, salt="out")
        )

        net_minutes = (new_out - new_in).total_seconds() / 60 - _BREAK_MINUTES
        net_hours = max(net_minutes / 60, 0.0)
        overtime = max(net_hours - _STANDARD_HOURS, 0.0)

        return dataclasses.replace(
            row,
            new_in=time_to_str(new_in),
            new_out=time_to_str(new_out),
            break_minutes=_BREAK_MINUTES,
            overtime_hours=round(overtime * 1.25, 2),
        )
