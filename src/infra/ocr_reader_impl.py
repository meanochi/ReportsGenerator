import os
import platform

import fitz  # PyMuPDF — renders PDF pages to images (no Poppler needed)
import pytesseract
from PIL import Image

from src.app.contracts.pdf_reader import IPDFReader
from src.domain.exceptions import ParsingError

_TESSERACT_CANDIDATES = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"),
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Tesseract\tesseract.exe"),
]


class OCRReaderImpl(IPDFReader):
    """
    Renders each PDF page via PyMuPDF then runs Tesseract OCR.
    No Poppler required.
    """

    def __init__(self) -> None:
        if platform.system() == "Windows":
            tesseract_cmd = next((p for p in _TESSERACT_CANDIDATES if os.path.exists(p)), None)
            if tesseract_cmd is None:
                raise EnvironmentError(
                    "Tesseract not found. Install from https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "Searched:\n  " + "\n  ".join(_TESSERACT_CANDIDATES)
                )
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def read_to_string(self, file_path: str) -> str:
        try:
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img, lang="heb+eng", config="--psm 6") + "\n"
            return text
        except Exception as exc:
            raise ParsingError(f"OCR failed for '{file_path}'. Error: {exc}") from exc
