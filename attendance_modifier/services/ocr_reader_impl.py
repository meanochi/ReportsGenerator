import pytesseract
from pdf2image import convert_from_path
from interfaces.pdf_reader import IPDFReader
from core.exceptions import ParsingError
import os
import platform

class OCRReaderImpl(IPDFReader):
    """Implementation of PDF reader using Tesseract OCR for scanned documents."""
    
    def __init__(self):
        # בדיקה אם אנחנו מריצים על Windows או על לינוקס (Docker)
        if platform.system() == "Windows":
            tesseract_cmd = r'C:\Users\329084941\AppData\Local\Programs\Tesseract\tesseract.exe'
            if os.path.exists(tesseract_cmd):
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            else:
                raise EnvironmentError(f"Tesseract not found at {tesseract_cmd}. Please install it.")
        else:
            # ב-Docker/Linux, Tesseract נמצא בנתיב המערכת
            pytesseract.pytesseract.tesseract_cmd = 'tesseract'

    def read_to_string(self, file_path: str) -> str:
        try:
            text = ""
            
            poppler_bin = None
            # ב-Windows צריך להגדיר נתיב ל-Poppler, ב-Docker הוא מותקן במערכת
            if platform.system() == "Windows":
                poppler_bin = r'M:\poppler\poppler-25.12.0\Library\bin'
            
            # אם poppler_bin הוא None (בלינוקס), הפונקציה תשתמש בברירת המחדל של המערכת
            pages = convert_from_path(file_path, dpi=300, poppler_path=poppler_bin)
            
            for page in pages:
                # הרצת OCR על התמונה (עברית + אנגלית)
                page_text = pytesseract.image_to_string(page, lang='heb+eng', config='--psm 6')
                text += page_text + "\n"
                
            return text
            
        except Exception as e:
            raise ParsingError(f"OCR failed for file '{file_path}'. Error: {str(e)}")