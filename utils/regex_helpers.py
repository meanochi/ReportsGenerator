import re

DATE_PATTERN = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b')

# עדכון חשוב: מאפשר גם נקודתיים וגם נקודה עשרונית בין השעות לדקות, ומתעלם מרווחים
TIME_PATTERN = re.compile(r'\b([0-1]?[0-9]|2[0-3])\s*[:.]\s*([0-5][0-9])\b')

def extract_times_from_line(line: str) -> list[str]:
    matches = TIME_PATTERN.findall(line)
    # גם אם ה-OCR מצא 8.30, אנחנו ננרמל את זה חזרה ל- 08:30 תקני
    normalized_times = [f"{int(hours):02d}:{minutes}" for hours, minutes in matches]
    return normalized_times