from interfaces.pdf_reader import IPDFReader
from interfaces.modifier import ITimeModifier
from interfaces.pdf_generator import IPDFGenerator
from services.classifier import ReportClassifier
from parsers.parser_factory import ParserFactory

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
        # 1. Extract Text
        raw_text = self.reader.read_to_string(input_pdf_path)
        
        # 2. Classify Report Type
        report_type = ReportClassifier.classify(raw_text)
        
        # 3. Parse Text to Objects (Strategy Pattern via Factory)
        parser = ParserFactory.get_parser(report_type)
        report_obj = parser.parse(raw_text)
        
        # 4. Transform (Modify data logically)
        self.modifier.apply_modifications(report_obj)
        
        # 5. Load / Generate new PDF
        self.generator.export(input_pdf_path, report_obj, output_pdf_path)