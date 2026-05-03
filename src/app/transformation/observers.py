from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.models import AttendanceRow


class TransformationObserver(ABC):
    @abstractmethod
    def on_row_transformed(self, before: AttendanceRow, after: AttendanceRow, report_type: str) -> None:
        ...


class CountingObserver(TransformationObserver):
    """Lightweight observer used by tests/diagnostics."""

    def __init__(self) -> None:
        self.transformed_rows = 0

    def on_row_transformed(self, before: AttendanceRow, after: AttendanceRow, report_type: str) -> None:
        self.transformed_rows += 1
