import re
from interfaces.parser import IReportParser
from core.models import AttendanceReport, AttendanceRow
from core.enums import ReportType
from utils.regex_helpers import DATE_PATTERN, extract_times_from_line
from utils.validators import is_valid_logical_date
from datetime import datetime, timedelta

_HEBREW_DAYS = {
    0: "שני", 1: "שלישי", 2: "רביעי",
    3: "חמישי", 4: "שישי", 5: "שבת", 6: "ראשון"
}
_DAY_NUM_PATTERN = re.compile(r'^\s*(\d{1,2})\s+יום\s+')
_DAY_NAME_PATTERN = re.compile('(' + '|'.join(_HEBREW_DAYS.values()) + ')')


def _reconstruct_dates(rows_data: list) -> list:
    """
    rows_data: list of dicts with keys: raw_date, day_name, original_in, original_out, raw_text_line
    For rows where raw_date is a full date (DD/MM/YYYY), use it as an anchor.
    For rows where raw_date is just a day number, reconstruct the full date
    by finding the nearest anchor and offsetting by the difference in day-of-month.
    """
    # Collect anchors: {day_of_month -> datetime}
    anchors = {}
    for r in rows_data:
        if '/' in r['raw_date'] and len(r['raw_date']) > 5:
            try:
                dt = datetime.strptime(r['raw_date'].replace('-', '/'), "%d/%m/%Y")
                anchors[dt.day] = dt
            except ValueError:
                pass

    result = []
    for r in rows_data:
        raw = r['raw_date']
        if '/' in raw and len(raw) > 5:
            # Already a full date
            dt = datetime.strptime(raw.replace('-', '/'), "%d/%m/%Y")
            day_name = _HEBREW_DAYS[dt.weekday()]
            result.append({**r, 'date': raw, 'day_name': day_name})
        elif anchors:
            # Day number only — reconstruct from nearest anchor
            day_num = int(raw)
            anchor_dt = min(anchors.values(), key=lambda d: abs(d.day - day_num))
            # Build candidate date in same month, or adjacent month if day_num > days in month
            try:
                candidate = anchor_dt.replace(day=day_num)
            except ValueError:
                result.append({**r, 'date': raw, 'day_name': r['day_name']})
                continue
            day_name = _HEBREW_DAYS[candidate.weekday()]
            result.append({**r, 'date': candidate.strftime("%d/%m/%Y"), 'day_name': day_name})
        else:
            result.append({**r, 'date': raw, 'day_name': r['day_name']})
    return result


class TypeAParser(IReportParser):
    def parse(self, raw_text: str) -> AttendanceReport:
        report = AttendanceReport(report_type=ReportType.TYPE_A, raw_text=raw_text)

        rows_data = []
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
                num_match = _DAY_NUM_PATTERN.match(line)
                if not num_match:
                    continue
                raw_date = num_match.group(1)

            try:
                time1 = datetime.strptime(times[0], "%H:%M")
                time2 = datetime.strptime(times[1], "%H:%M")
                rows_data.append({
                    'raw_date': raw_date,
                    'day_name': day_name,
                    'original_in': min(time1, time2).strftime("%H:%M"),
                    'original_out': max(time1, time2).strftime("%H:%M"),
                    'raw_text_line': line
                })
            except ValueError:
                continue

        for r in _reconstruct_dates(rows_data):
            report.rows.append(AttendanceRow(
                date=r['date'],
                original_in=r['original_in'],
                original_out=r['original_out'],
                raw_text_line=r['raw_text_line'],
                day_name=r['day_name']
            ))

        return report