from abc import ABC, abstractmethod

from src.domain.models import AttendanceReport


class ITimeModifier(ABC):
    @abstractmethod
    def apply_modifications(self, report: AttendanceReport) -> AttendanceReport:
        """Returns a new AttendanceReport with modified attendance times."""
