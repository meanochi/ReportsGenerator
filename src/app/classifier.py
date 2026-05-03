import re

from src.domain.enums import ReportType
from src.domain.exceptions import ClassificationError


class ReportClassifier:
    """Classifies the report type based on OCR text."""

    SHORT_YEAR_PATTERN = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2}\b")
    LONG_YEAR_PATTERN = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b")

    @staticmethod
    def classify(raw_text: str) -> ReportType:
        short_year_matches = len(ReportClassifier.SHORT_YEAR_PATTERN.findall(raw_text))
        long_year_matches = len(ReportClassifier.LONG_YEAR_PATTERN.findall(raw_text))

        if long_year_matches > 3 and long_year_matches > short_year_matches:
            return ReportType.TYPE_A
        if short_year_matches > 3 and short_year_matches > long_year_matches:
            return ReportType.TYPE_B

        if "הנשר" in raw_text:
            return ReportType.TYPE_A
        if "כרטיס עובד" in raw_text or "כרטיס" in raw_text:
            return ReportType.TYPE_B

        type_a_row_pattern = re.compile(r"\d+\s+יום\s+\S+")
        if len(type_a_row_pattern.findall(raw_text)) > 2:
            return ReportType.TYPE_A

        raise ClassificationError("Could not determine report type. Patterns and keywords not found.")
