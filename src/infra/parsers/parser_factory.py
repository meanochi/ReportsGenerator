from src.app.contracts.parser import IReportParser
from src.domain.enums import ReportType
from src.infra.parsers.type_a_parser import TypeAParser
from src.infra.parsers.type_b_parser import TypeBParser


class ParserFactory:
    """Factory to return the correct parser strategy based on report type."""

    _registry = {
        ReportType.TYPE_A: TypeAParser,
        ReportType.TYPE_B: TypeBParser,
    }

    @classmethod
    def register_parser(cls, report_type: ReportType, parser_cls: type[IReportParser]) -> None:
        cls._registry[report_type] = parser_cls

    @classmethod
    def get_parser(cls, report_type: ReportType) -> IReportParser:
        parser_cls = cls._registry.get(report_type)
        if parser_cls is None:
            raise ValueError(f"No parser implemented for report type: {report_type}")
        return parser_cls()
