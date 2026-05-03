from config.rules import RULES
from src.app.transformation.base_strategy import BaseTransformationStrategy
from src.domain.exceptions import TransformationError
from src.domain.models import AttendanceRow
from utils.time_utils import str_to_time


class ValidatingStrategyDecorator(BaseTransformationStrategy):
    """Wraps a strategy and validates the result before returning it."""

    def __init__(self, inner: BaseTransformationStrategy) -> None:
        self._inner = inner

    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        result = self._inner.transform_row(row)
        self._validate(result)
        return result

    def _validate(self, row: AttendanceRow) -> None:
        if not row.new_in or not row.new_out:
            return

        entry = str_to_time(row.new_in)
        exit_ = str_to_time(row.new_out)

        if exit_ <= entry:
            raise TransformationError(
                f"[{row.date}] exit_time ({row.new_out}) must be after entry_time ({row.new_in})."
            )

        work_hours = (exit_ - entry).total_seconds() / 3600
        if work_hours > RULES.MAX_WORK_HOURS:
            raise TransformationError(
                f"[{row.date}] work duration {work_hours:.1f}h exceeds maximum {RULES.MAX_WORK_HOURS}h."
            )

        if row.break_minutes is not None and row.break_minutes > RULES.MAX_BREAK_MINUTES:
            raise TransformationError(
                f"[{row.date}] break_minutes ({row.break_minutes}) exceeds logical bound of {RULES.MAX_BREAK_MINUTES}."
            )
