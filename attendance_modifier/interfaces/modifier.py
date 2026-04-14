from abc import ABC, abstractmethod
from core.models import AttendanceReport

class ITimeModifier(ABC):
    @abstractmethod
    def apply_modifications(self, report: AttendanceReport) -> None:
        """Applies business rules to modify attendance times."""
        pass