from datetime import datetime

def is_valid_logical_date(date_str: str) -> bool:
    """
    Validates that a date string is an actual calendar date,
    and falls within a logical timeframe (e.g., not in the distant past/future).
    """
    clean_date = date_str.replace('-', '/')
    parsed_date = None
    
    # 1. בדיקת תקינות קלנדרית
    try:
        parsed_date = datetime.strptime(clean_date, "%d/%m/%Y")
    except ValueError:
        try:
            parsed_date = datetime.strptime(clean_date, "%d/%m/%y")
        except ValueError:
            # ה-OCR קרא תאריך שלא קיים בלוח השנה (כמו 32/01/22)
            return False
            
    # 2. בדיקת לוגיקה עסקית (Sanity Check)
    current_year = datetime.now().year
    
    # אנחנו מניחים שדוחות נוכחות רלוונטיים לשנים האחרונות ולא לעתיד הרחוק
    if not (2000 <= parsed_date.year <= current_year + 1):
        return False
        
    return True