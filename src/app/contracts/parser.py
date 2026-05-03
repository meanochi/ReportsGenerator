from abc import ABC, abstractmethod

from src.domain.models import AttendanceReport


class IReportParser(ABC):
    @abstractmethod
    def parse(self, raw_text: str) -> AttendanceReport:
        """Parses raw text into an AttendanceReport object."""
