from src.app.classifier import ReportClassifier
from src.app.contracts.modifier import ITimeModifier
from src.app.contracts.pdf_generator import IPDFGenerator
from src.app.contracts.pdf_reader import IPDFReader
from src.infra.parsers.parser_factory import ParserFactory


class ReportProcessingPipeline:
    """
    The Orchestrator. Manages the ETL flow of the PDF report.
    Uses Dependency Injection to receive its components.
    """

    def __init__(self, reader: IPDFReader, modifier: ITimeModifier, generator: IPDFGenerator):
        self.reader = reader
        self.modifier = modifier
        self.generator = generator

    def process(self, input_pdf_path: str, output_pdf_path: str) -> None:
        raw_text = self.reader.read_to_string(input_pdf_path)
        report_type = ReportClassifier.classify(raw_text)
        parser = ParserFactory.get_parser(report_type)
        report_obj = parser.parse(raw_text)
        report_obj = self.modifier.apply_modifications(report_obj)
        self.generator.export(input_pdf_path, report_obj, output_pdf_path)
