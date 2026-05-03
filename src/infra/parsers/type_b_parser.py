from typing import Optional

from src.domain.enums import ReportType
from src.infra.parsers.base_parser import BaseParser, RowPayload
from utils.regex_helpers import DATE_PATTERN, extract_times_from_line
from utils.validators import is_valid_logical_date


class TypeBParser(BaseParser):
    def report_type(self) -> ReportType:
        return ReportType.TYPE_B

    def extract_row_payload(self, line: str) -> Optional[RowPayload]:
        date_match = DATE_PATTERN.search(line)
        times = extract_times_from_line(line)
        if not date_match or len(times) < 2:
            return None

        extracted_date = date_match.group(1)
        if not is_valid_logical_date(extracted_date):
            return None

        try:
            self._normalized_time_pair(times[0], times[1])
        except ValueError:
            return None

        return {
            "date": extracted_date,
            "original_in": times[0],
            "original_out": times[1],
            "raw_text_line": line,
        }
