from abc import ABC, abstractmethod
from core.models import AttendanceReport

class IReportParser(ABC):
    @abstractmethod
    def parse(self, raw_text: str) -> AttendanceReport:
        """Parses raw text into an AttendanceReport object."""
        pass