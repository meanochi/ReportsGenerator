from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Tuple, TypedDict

from src.app.contracts.parser import IReportParser
from src.domain.enums import ReportType
from src.domain.models import AttendanceReport, AttendanceRow


class RowPayload(TypedDict, total=False):
    date: str
    original_in: str
    original_out: str
    day_name: str
    raw_text_line: str


class BaseParser(IReportParser, ABC):
    """Template Method parser skeleton."""

    def parse(self, raw_text: str) -> AttendanceReport:
        report = AttendanceReport(report_type=self.report_type(), raw_text=raw_text)
        for line in raw_text.splitlines():
            payload = self.extract_row_payload(line)
            if payload is None:
                continue

            original_in, original_out = self._normalized_time_pair(
                payload["original_in"], payload["original_out"]
            )
            report.rows.append(
                AttendanceRow(
                    date=payload["date"],
                    original_in=original_in,
                    original_out=original_out,
                    raw_text_line=payload.get("raw_text_line", line),
                    day_name=payload.get("day_name"),
                )
            )
        return report

    @staticmethod
    def _normalized_time_pair(time_a: str, time_b: str) -> Tuple[str, str]:
        t1 = datetime.strptime(time_a, "%H:%M")
        t2 = datetime.strptime(time_b, "%H:%M")
        return min(t1, t2).strftime("%H:%M"), max(t1, t2).strftime("%H:%M")

    @abstractmethod
    def report_type(self) -> ReportType:
        """Return a ReportType value."""

    @abstractmethod
    def extract_row_payload(self, line: str) -> Optional[RowPayload]:
        """Return normalized row payload or None."""
