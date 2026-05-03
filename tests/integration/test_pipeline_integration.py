import os
from pathlib import Path

from src.app.contracts.pdf_generator import IPDFGenerator
from src.app.contracts.pdf_reader import IPDFReader
from src.app.modifier import DeterministicTimeModifier
from src.app.pipeline import ReportProcessingPipeline
from src.domain.models import AttendanceReport


class _FakeReader(IPDFReader):
    def read_to_string(self, file_path: str) -> str:
        return Path(file_path).read_text(encoding="utf-8")


class _CaptureGenerator(IPDFGenerator):
    def __init__(self) -> None:
        self.last_report: AttendanceReport | None = None

    def export(self, original_path: str, report: AttendanceReport, output_path: str) -> None:
        self.last_report = report


def test_pipeline_processes_full_flow_type_b() -> None:
    fixture = Path(__file__).parent / "fixtures" / "type_b_ocr.txt"
    reader = _FakeReader()
    modifier = DeterministicTimeModifier()
    generator = _CaptureGenerator()
    pipeline = ReportProcessingPipeline(reader, modifier, generator)

    pipeline.process(str(fixture), "output.pdf")

    assert generator.last_report is not None
    assert len(generator.last_report.rows) == 4
    assert all(r.new_in is not None for r in generator.last_report.rows)
    assert all(r.new_out is not None for r in generator.last_report.rows)


def test_pipeline_seed_changes_deterministic_output() -> None:
    fixture = Path(__file__).parent / "fixtures" / "type_b_ocr.txt"
    reader = _FakeReader()

    os.environ["ATTENDANCE_VARIATION_SEED"] = "v1"
    generator_v1 = _CaptureGenerator()
    ReportProcessingPipeline(reader, DeterministicTimeModifier(), generator_v1).process(str(fixture), "out1.pdf")
    assert generator_v1.last_report is not None
    result_v1 = [r.new_in for r in generator_v1.last_report.rows]

    os.environ["ATTENDANCE_VARIATION_SEED"] = "v2"
    generator_v2 = _CaptureGenerator()
    ReportProcessingPipeline(reader, DeterministicTimeModifier(), generator_v2).process(str(fixture), "out2.pdf")
    assert generator_v2.last_report is not None
    result_v2 = [r.new_in for r in generator_v2.last_report.rows]

    assert result_v1 != result_v2
