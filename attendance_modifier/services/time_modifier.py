from interfaces.modifier import ITimeModifier
from core.models import AttendanceReport
from utils.time_utils import str_to_time, time_to_str, get_deterministic_delta
from datetime import timedelta

class DeterministicTimeModifier(ITimeModifier):
    """
    Modifies attendance times deterministically.
    Ensures logical validity: end_time > start_time and valid working hours.
    """
    
    def apply_modifications(self, report: AttendanceReport) -> None:
        for row in report.rows:
            if not row.original_in or not row.original_out:
                continue # מתעלם מימים שאין בהם כניסה או יציאה
                
            dt_in = str_to_time(row.original_in)
            dt_out = str_to_time(row.original_out)
            
            # יצירת שינוי דטרמיניסטי מבוסס על התאריך
            delta_in_minutes = get_deterministic_delta(row.date, salt="in")
            delta_out_minutes = get_deterministic_delta(row.date, salt="out")
            
            new_dt_in = dt_in + timedelta(minutes=delta_in_minutes)
            new_dt_out = dt_out + timedelta(minutes=delta_out_minutes)
            
            # ולידציה 1: שעת סיום חייבת להיות אחרי שעת התחלה
            if new_dt_out <= new_dt_in:
                new_dt_out = new_dt_in + timedelta(hours=1) # מינימום שעת עבודה אחת
                
            # ולידציה 2: טווח שעות סביר (נניח מקסימום 12 שעות)
            work_duration = (new_dt_out - new_dt_in).total_seconds() / 3600
            if work_duration > 12:
                new_dt_out = new_dt_in + timedelta(hours=12)
                
            row.new_in = time_to_str(new_dt_in)
            row.new_out = time_to_str(new_dt_out)