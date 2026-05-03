import dataclasses

from src.app.contracts.modifier import ITimeModifier
from src.app.transformation.observers import TransformationObserver
from src.app.transformation.transformation_service import TransformationService
from src.app.transformation.type_a_strategy import TypeATransformationStrategy
from src.app.transformation.type_b_strategy import TypeBTransformationStrategy
from src.app.transformation.validating_decorator import ValidatingStrategyDecorator
from src.domain.models import AttendanceReport


class DeterministicTimeModifier(ITimeModifier):
    """
    Modifies attendance times deterministically.
    Ensures logical validity: end_time > start_time and valid working hours.
    """

    def __init__(self, observers: list[TransformationObserver] | None = None) -> None:
        strategy_registry = {
            "TYPE_A": ValidatingStrategyDecorator(TypeATransformationStrategy()),
            "TYPE_B": ValidatingStrategyDecorator(TypeBTransformationStrategy()),
        }
        self._service = TransformationService(strategy_registry, observers=observers or [])

    def apply_modifications(self, report: AttendanceReport) -> AttendanceReport:
        transformed = self._service.transform(report.rows, report.report_type.name)
        return dataclasses.replace(report, rows=transformed)
