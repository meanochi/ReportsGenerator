import os
from datetime import datetime
from interfaces.pdf_generator import IPDFGenerator
from core.models import AttendanceReport
from core.enums import ReportType

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class PDFGeneratorImpl(IPDFGenerator):
    def __init__(self):
        self._register_hebrew_font()

    def _register_hebrew_font(self):
        try:
            font_path = "C:\\Windows\\Fonts\\arial.ttf" if os.name == 'nt' else "Arial.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('HebrewFont', font_path))
                self.font_name = 'HebrewFont'
            else:
                self.font_name = 'Helvetica'
        except Exception:
            self.font_name = 'Helvetica'

    def _reverse_hebrew(self, text: str) -> str:
        return text[::-1]

    def _get_hebrew_day(self, date_str: str) -> str:
        """
        Parses the date string (handles both YY and YYYY formats)
        and returns the correct Hebrew day of the week.
        """
        clean_date = date_str.replace('-', '/')
        dt = None
        
        # מנסה לפענח תאריך עם שנה מלאה (למשל 02/10/2022)
        try:
            dt = datetime.strptime(clean_date, "%d/%m/%Y")
        except ValueError:
            # מנסה לפענח תאריך עם שנה קצרה (למשל 1/9/22)
            try:
                dt = datetime.strptime(clean_date, "%d/%m/%y")
            except ValueError:
                return "" # אם התאריך לא תקין בכלל, נחזיר ריק

        # ב-Python: 0=Monday, 1=Tuesday, ... 6=Sunday
        days_map = {
            0: "שני",
            1: "שלישי",
            2: "רביעי",
            3: "חמישי",
            4: "שישי",
            5: "שבת",
            6: "ראשון"
        }
        
        # מחזיר את היום אחרי היפוך להתאמה לספריית יצירת ה-PDF
        return self._reverse_hebrew(days_map[dt.weekday()])

    def export(self, original_path: str, report: AttendanceReport, output_path: str) -> None:
        page_layout = landscape(A4) if report.report_type == ReportType.TYPE_A else A4
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=page_layout,
            rightMargin=20, leftMargin=20, topMargin=30, bottomMargin=30
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_str = "ג.ע. הנשר כח אדם בע\"מ - דוח מעודכן" if report.report_type == ReportType.TYPE_A else "כרטיס עובד לחודש - דוח מעודכן"
        title = Paragraph(f"<font name='{self.font_name}' size='16'><b>{self._reverse_hebrew(title_str)}</b></font>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        if report.report_type == ReportType.TYPE_A:
            elements.append(self._generate_type_a_table(report))
        else:
            elements.append(self._generate_type_b_table(report))
            
        doc.build(elements)

    def _generate_type_a_table(self, report: AttendanceReport) -> Table:
        """Generates the complex structure for Report Type A (Includes Overtime)"""
        # הוספנו את עמודת "יום"
        headers = ["תאריך", "יום", "מקום עבודה", "כניסה", "יציאה", "הפסקה", "סה\"כ", "%001", "%521", "%051"]
        headers = [self._reverse_hebrew(h) for h in headers]
        headers.reverse() 
        
        data = [headers]
        time_format = "%H:%M"
        
        for row in report.rows:
            if not row.new_in or not row.new_out:
                continue
                
            t_in = datetime.strptime(row.new_in, time_format)
            t_out = datetime.strptime(row.new_out, time_format)
            
            total_hours = max((t_out - t_in).total_seconds() / 3600.0 - 0.5, 0)
            base_100 = min(total_hours, 8.0)
            over_125 = min(max(total_hours - 8.0, 0), 2.0)
            over_150 = max(total_hours - 10.0, 0)
            
            row_data = [
                row.date,
                self._get_hebrew_day(row.date),           # <--- שאיבת היום המחושב
                self._reverse_hebrew("כללי"), 
                row.new_in,
                row.new_out,
                "00:30",
                f"{total_hours:.2f}",
                f"{base_100:.2f}",
                f"{over_125:.2f}",
                f"{over_150:.2f}"
            ]
            row_data.reverse()
            data.append(row_data)

        # הענקנו רוחב אחיד ל-10 עמודות (סה"כ 600 פיקסלים בערך, נכנס יופי ב-Landscape)
        table = Table(data, colWidths=[60]*10)
        table.setStyle(self._get_base_table_style())
        return table

    def _generate_type_b_table(self, report: AttendanceReport) -> Table:
        """Generates the structure for Report Type B (Simple In/Out/Total)"""
        headers = ["תאריך", "יום", "שעת כניסה", "שעת יציאה", "סה\"כ שעות", "הערות"]
        headers = [self._reverse_hebrew(h) for h in headers]
        headers.reverse()
        
        data = [headers]
        time_format = "%H:%M"
        
        for row in report.rows:
            if not row.new_in or not row.new_out:
                continue
                
            t_in = datetime.strptime(row.new_in, time_format)
            t_out = datetime.strptime(row.new_out, time_format)
            
            total_hours = (t_out - t_in).total_seconds() / 3600.0
            
            row_data = [
                row.date,
                self._get_hebrew_day(row.date), # <--- שאיבת היום המחושב
                row.new_in,
                row.new_out,
                f"{total_hours:.2f}",
                ""  
            ]
            row_data.reverse()
            data.append(row_data)

        table = Table(data, colWidths=[80, 60, 80, 80, 80, 100])
        table.setStyle(self._get_base_table_style())
        return table

    def _get_base_table_style(self) -> TableStyle:
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#A6A6A6")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])