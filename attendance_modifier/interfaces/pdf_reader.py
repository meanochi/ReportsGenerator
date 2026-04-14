from abc import ABC, abstractmethod

class IPDFReader(ABC):
    @abstractmethod
    def read_to_string(self, file_path: str) -> str:
        """Extracts and returns all text from the PDF."""
        pass