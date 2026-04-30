from typing import Dict, List
from core.models import AttendanceRow
from core.exceptions import TransformationError
from services.transformation.base_strategy import BaseTransformationStrategy


class TransformationService:
    """
    Applies the correct strategy to every row based on a report-type token.
    Open/Closed: adding a new type only requires a new strategy + one registry entry.
    """

    def __init__(self, strategy_registry: Dict[str, BaseTransformationStrategy]) -> None:
        self._registry = strategy_registry

    def transform(self, rows: List[AttendanceRow], report_type: str) -> List[AttendanceRow]:
        strategy = self._registry.get(report_type)
        if strategy is None:
            raise TransformationError(f"No strategy registered for report type '{report_type}'.")

        return [strategy.transform_row(row) for row in rows]
