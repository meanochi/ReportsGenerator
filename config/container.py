from __future__ import annotations

from src.app.transformation.observers import CountingObserver


class Container:
    """
    Composition root for the application.
    Main should depend on this container instead of constructing services inline.
    """

    def __init__(self) -> None:
        self._transformation_counter = CountingObserver()

    def build_pipeline(self):
        from src.app.modifier import DeterministicTimeModifier
        from src.app.pipeline import ReportProcessingPipeline
        from src.infra.ocr_reader_impl import OCRReaderImpl
        from src.infra.pdf_generator_impl import PDFGeneratorImpl

        reader = OCRReaderImpl()
        modifier = DeterministicTimeModifier(observers=[self._transformation_counter])
        generator = PDFGeneratorImpl()
        return ReportProcessingPipeline(reader, modifier, generator)
