import pytesseract
from pdf2image import convert_from_path
from interfaces.pdf_reader import IPDFReader
from core.exceptions import ParsingError
import os

class OCRReaderImpl(IPDFReader):
    """Implementation of PDF reader using Tesseract OCR for scanned documents."""
    
    def __init__(self):
        tesseract_cmd = r'C:\Users\329084941\AppData\Local\Programs\Tesseract\tesseract.exe'
        if os.path.exists(tesseract_cmd):
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            raise EnvironmentError(f"Tesseract not found at {tesseract_cmd}. Please install it.")

    def read_to_string(self, file_path: str) -> str:
        try:
            text = ""
            
            # הוספנו כאן את הנתיב המפורש לתיקיית bin של poppler
            poppler_bin = r'M:\poppler\poppler-25.12.0\Library\bin'
            
            pages = convert_from_path(file_path, dpi=300, poppler_path=poppler_bin)
            
            for page in pages:
                # הרצת OCR על התמונה (עברית + אנגלית)
                # הוספנו את ה-config שמסדר קריאת טבלאות
                page_text = pytesseract.image_to_string(page, lang='heb+eng', config='--psm 6')
                text += page_text + "\n"
                
            return text
            
        except Exception as e:
            raise ParsingError(f"OCR failed for file '{file_path}'. Error: {str(e)}")