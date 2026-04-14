from interfaces.parser import IReportParser
from core.enums import ReportType
from parsers.type_a_parser import TypeAParser
from parsers.type_b_parser import TypeBParser

class ParserFactory:
    """Factory to return the correct parser strategy based on report type."""
    
    @staticmethod
    def get_parser(report_type: ReportType) -> IReportParser:
        if report_type == ReportType.TYPE_A:
            return TypeAParser()
        elif report_type == ReportType.TYPE_B:
            return TypeBParser()
        
        raise ValueError(f"No parser implemented for report type: {report_type}")