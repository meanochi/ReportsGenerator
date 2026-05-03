import dataclasses
from datetime import timedelta

from src.app.transformation.base_strategy import BaseTransformationStrategy
from src.domain.models import AttendanceRow
from utils.time_utils import get_deterministic_delta, str_to_time, time_to_str


class TypeATransformationStrategy(BaseTransformationStrategy):
    """Simple time-shift strategy for Type A (Nesher HR) reports."""

    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        if not row.original_in or not row.original_out:
            return row

        new_in = str_to_time(row.original_in) + timedelta(
            minutes=get_deterministic_delta(row.date, salt="in")
        )
        new_out = str_to_time(row.original_out) + timedelta(
            minutes=get_deterministic_delta(row.date, salt="out")
        )

        return dataclasses.replace(
            row,
            new_in=time_to_str(new_in),
            new_out=time_to_str(new_out),
        )
