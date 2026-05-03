from abc import ABC, abstractmethod

from src.domain.models import AttendanceReport


class IPDFGenerator(ABC):
    @abstractmethod
    def export(self, original_path: str, report: AttendanceReport, output_path: str) -> None:
        """Generates the new PDF based on the original structure and new data."""
