import re
from datetime import datetime, timedelta
from typing import Optional

from src.domain.enums import ReportType
from src.domain.models import AttendanceReport, AttendanceRow
from src.infra.parsers.base_parser import BaseParser, RowPayload
from utils.regex_helpers import DATE_PATTERN, extract_times_from_line
from utils.validators import is_valid_logical_date

_HEBREW_DAYS = {
    0: "שני",
    1: "שלישי",
    2: "רביעי",
    3: "חמישי",
    4: "שישי",
    5: "שבת",
    6: "ראשון",
}
_DAY_NAME_PATTERN = re.compile("(" + "|".join(_HEBREW_DAYS.values()) + ")")


def _reconstruct_dates(rows_data: list[dict]) -> list[dict]:
    """
    Fill in missing dates using position-based interpolation between anchor dates.
    Anchor dates are rows where OCR successfully read a full dd/mm/yyyy date.
    Rows without a full date get a date interpolated from their position between anchors.
    """
    anchors: dict[int, datetime] = {}
    for i, row_data in enumerate(rows_data):
        raw = row_data["raw_date"]
        if "/" in raw and len(raw) > 5:
            try:
                anchors[i] = datetime.strptime(raw.replace("-", "/"), "%d/%m/%Y")
            except ValueError:
                pass

    result: list[dict] = []
    for i, row_data in enumerate(rows_data):
        raw = row_data["raw_date"]
        if "/" in raw and len(raw) > 5:
            dt = datetime.strptime(raw.replace("-", "/"), "%d/%m/%Y")
            result.append({**row_data, "date": dt.strftime("%d/%m/%Y"), "day_name": _HEBREW_DAYS[dt.weekday()]})
            continue

        # Interpolate between nearest anchors before and after this row
        before = {k: v for k, v in anchors.items() if k < i}
        after  = {k: v for k, v in anchors.items() if k > i}

        if before and after:
            prev_i, prev_dt = max(before.items(), key=lambda x: x[0])
            next_i, next_dt = min(after.items(),  key=lambda x: x[0])
            span = (next_dt - prev_dt).days
            step = i - prev_i
            total_steps = next_i - prev_i
            dt = prev_dt + timedelta(days=round(span * step / total_steps))
        elif before:
            prev_i, prev_dt = max(before.items(), key=lambda x: x[0])
            dt = prev_dt + timedelta(days=(i - prev_i))
        elif after:
            next_i, next_dt = min(after.items(), key=lambda x: x[0])
            dt = next_dt - timedelta(days=(next_i - i))
        else:
            result.append({**row_data, "date": raw, "day_name": row_data.get("day_name", "")})
            continue

        result.append({**row_data, "date": dt.strftime("%d/%m/%Y"), "day_name": _HEBREW_DAYS[dt.weekday()]})
    return result


class TypeAParser(BaseParser):
    def report_type(self) -> ReportType:
        return ReportType.TYPE_A

    def parse(self, raw_text: str) -> AttendanceReport:
        report = AttendanceReport(report_type=self.report_type(), raw_text=raw_text)
        rows_data: list[dict] = []

        for line in raw_text.splitlines():
            times = extract_times_from_line(line)
            if len(times) < 2:
                continue

            day_match = _DAY_NAME_PATTERN.search(line)
            day_name = day_match.group(1) if day_match else ""

            date_match = DATE_PATTERN.search(line)
            if date_match:
                raw_date = date_match.group(1)
                if not is_valid_logical_date(raw_date):
                    continue
            else:
                # No full date — mark unknown; _reconstruct_dates will interpolate
                raw_date = "?"

            try:
                # Take the last two times: Type A lines have break time before entry/exit
                # e.g. "00:30 16:00 08:00" → skip 00:30, take 16:00 & 08:00
                original_in, original_out = self._normalized_time_pair(times[-2], times[-1])
            except ValueError:
                continue

            # Skip summary/header lines where both times are identical (e.g. 00:00 00:00)
            if original_in == original_out:
                continue

            rows_data.append({
                "raw_date": raw_date,
                "day_name": day_name,
                "original_in": original_in,
                "original_out": original_out,
                "raw_text_line": line,
            })

        for row_data in _reconstruct_dates(rows_data):
            report.rows.append(
                AttendanceRow(
                    date=row_data["date"],
                    original_in=row_data["original_in"],
                    original_out=row_data["original_out"],
                    raw_text_line=row_data.get("raw_text_line", ""),
                    day_name=row_data.get("day_name"),
                )
            )
        return report

    def extract_row_payload(self, line: str) -> Optional[RowPayload]:
        return None
