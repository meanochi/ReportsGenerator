import fitz  # PyMuPDF
from interfaces.pdf_reader import IPDFReader
from core.exceptions import ParsingError

class PDFReaderImpl(IPDFReader):
    """Implementation of PDF reader using PyMuPDF to extract text."""
    
    def read_to_string(self, file_path: str) -> str:
        try:
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text("text") + "\n"
            return text
        except Exception as e:
            raise ParsingError(f"Failed to read PDF file '{file_path}': {str(e)}")