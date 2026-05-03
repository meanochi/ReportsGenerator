from src.app.transformation.base_strategy import BaseTransformationStrategy
from src.app.transformation.observers import CountingObserver
from src.app.transformation.transformation_service import TransformationService
from src.app.transformation.type_a_strategy import TypeATransformationStrategy
from src.app.transformation.validating_decorator import ValidatingStrategyDecorator
from src.domain.enums import ReportType
from src.domain.models import AttendanceRow
from src.infra.parsers.parser_factory import ParserFactory


class _NoOpStrategy(BaseTransformationStrategy):
    def transform_row(self, row: AttendanceRow) -> AttendanceRow:
        return row


def test_parser_factory_registry_supports_registration() -> None:
    class _DummyParser:
        def parse(self, raw_text: str):  # pragma: no cover - not used by test
            return raw_text

    ParserFactory.register_parser(ReportType.UNKNOWN, _DummyParser)
    parser = ParserFactory.get_parser(ReportType.UNKNOWN)
    assert isinstance(parser, _DummyParser)


def test_decorator_implements_strategy_contract() -> None:
    decorated = ValidatingStrategyDecorator(TypeATransformationStrategy())
    assert isinstance(decorated, BaseTransformationStrategy)


def test_transformation_service_notifies_observer() -> None:
    observer = CountingObserver()
    service = TransformationService({"TYPE_B": _NoOpStrategy()}, observers=[observer])
    rows = [
        AttendanceRow(
            date="01/01/2024",
            original_in="08:00",
            original_out="16:00",
            raw_text_line="row 1",
        ),
        AttendanceRow(
            date="02/01/2024",
            original_in="08:10",
            original_out="16:10",
            raw_text_line="row 2",
        ),
    ]

    result = service.transform(rows, "TYPE_B")
    assert len(result) == 2
    assert observer.transformed_rows == 2
