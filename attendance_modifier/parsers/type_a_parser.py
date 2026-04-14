from interfaces.parser import IReportParser
from core.models import AttendanceReport, AttendanceRow
from core.enums import ReportType
from utils.regex_helpers import DATE_PATTERN, extract_times_from_line
from utils.validators import is_valid_logical_date  # ייבוא הולידציה
from datetime import datetime

class TypeAParser(IReportParser):
    def parse(self, raw_text: str) -> AttendanceReport:
        report = AttendanceReport(report_type=ReportType.TYPE_A, raw_text=raw_text)
        
        for line in raw_text.splitlines():
            date_match = DATE_PATTERN.search(line)
            times = extract_times_from_line(line)
            
            if date_match and len(times) >= 2:
                extracted_date = date_match.group(1)
                
                # --- ולידציה של התאריך ---
                if not is_valid_logical_date(extracted_date):
                    continue # דילוג על השורה אם התאריך לא חוקי
                    
                try:
                    time1 = datetime.strptime(times[0], "%H:%M")
                    time2 = datetime.strptime(times[1], "%H:%M")
                    
                    original_in = min(time1, time2).strftime("%H:%M")
                    original_out = max(time1, time2).strftime("%H:%M")
                    
                    row = AttendanceRow(
                        date=extracted_date,
                        original_in=original_in,
                        original_out=original_out,
                        raw_text_line=line
                    )
                    report.rows.append(row)
                except ValueError:
                    continue
                
        return report