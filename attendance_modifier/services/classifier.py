import re
from core.enums import ReportType
from core.exceptions import ClassificationError

class ReportClassifier:
    """
    Classifies the report type based on OCR text.
    Uses Data-Pattern matching instead of keywords, as OCR Hebrew text is often noisy.
    """
    
    # חיפוש תאריכים בפורמט D/M/YY (כמו 1/9/22)
    SHORT_YEAR_PATTERN = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2}\b')
    
    # חיפוש תאריכים בפורמט DD/MM/YYYY (כמו 02/10/2022)
    LONG_YEAR_PATTERN = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b')

    @staticmethod
    def classify(raw_text: str) -> ReportType:
        # ספירת מופעים של כל סוג תאריך בטקסט שחולץ מה-OCR
        short_year_matches = len(ReportClassifier.SHORT_YEAR_PATTERN.findall(raw_text))
        long_year_matches = len(ReportClassifier.LONG_YEAR_PATTERN.findall(raw_text))

        # אם יש יותר תאריכים ארוכים -> סוג א' (הנשר)
        if long_year_matches > 3 and long_year_matches > short_year_matches:
            return ReportType.TYPE_A
            
        # אם יש יותר תאריכים קצרים -> סוג ב' (כרטיס עובד)
        elif short_year_matches > 3 and short_year_matches > long_year_matches:
            return ReportType.TYPE_B
            
        # אם המערכת עדיין לא בטוחה, ננסה את מילות המפתח בתור גיבוי (Fallback)
        def is_match(keyword: str) -> bool:
            return keyword in raw_text or keyword[::-1] in raw_text

        if is_match("ג.ע. הנשר") or is_match("הנשר כח אדם"):
            return ReportType.TYPE_A
        elif is_match("כרטיס עובד") or is_match("סה\"כימיעבודה"): # הותאם ל-OCR
            return ReportType.TYPE_B
        
        # הדפסת DEBUG במקרה של כישלון מוחלט
        print("\n--- DEBUG: Text extracted from PDF (First 300 chars) ---")
        print(raw_text[:300])
        print("--------------------------------------------------------\n")
        
        raise ClassificationError("Could not determine report type. Patterns and keywords not found.")