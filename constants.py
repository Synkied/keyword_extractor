from pdf.pdf_extraction import PDFExtractor


UNWANTED_CHARS_REGEX = '[.,-:;–\'!?<>)(\][}{/]'

HANDLED_FILE_TYPES = {
    'pdf': PDFExtractor,
}
