from typing import Dict, List, Optional

from src.app.transformation.base_strategy import BaseTransformationStrategy
from src.app.transformation.observers import TransformationObserver
from src.domain.exceptions import TransformationError
from src.domain.models import AttendanceRow


class TransformationService:
    """
    Applies the correct strategy to every row based on a report-type token.
    Open/Closed: adding a new type only requires a new strategy + one registry entry.
    """

    def __init__(
        self,
        strategy_registry: Dict[str, BaseTransformationStrategy],
        observers: Optional[List[TransformationObserver]] = None,
    ) -> None:
        self._registry = strategy_registry
        self._observers = observers or []

    def transform(self, rows: List[AttendanceRow], report_type: str) -> List[AttendanceRow]:
        strategy = self._registry.get(report_type)
        if strategy is None:
            raise TransformationError(f"No strategy registered for report type '{report_type}'.")

        transformed: List[AttendanceRow] = []
        for row in rows:
            new_row = strategy.transform_row(row)
            for observer in self._observers:
                observer.on_row_transformed(row, new_row, report_type)
            transformed.append(new_row)
        return transformed
