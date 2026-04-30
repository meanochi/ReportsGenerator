from abc import ABC, abstractmethod
from core.models import AttendanceRow


class BaseTransformationStrategy(ABC):
    @abstractmethod
    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        ...
