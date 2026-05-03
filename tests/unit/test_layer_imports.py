from src.app.pipeline import ReportProcessingPipeline
from src.domain.enums import ReportType
from src.domain.models import AttendanceReport, AttendanceRow
from src.infra.parsers.parser_factory import ParserFactory


def test_layer_packages_are_importable() -> None:
    assert ReportProcessingPipeline is not None
    assert ParserFactory is not None


def test_domain_exports_are_usable() -> None:
    row = AttendanceRow(
        date="01/01/2024",
        original_in="08:00",
        original_out="16:00",
        raw_text_line="sample",
    )
    report = AttendanceReport(report_type=ReportType.TYPE_B, rows=[row], raw_text="raw")
    assert report.rows[0].date == "01/01/2024"
