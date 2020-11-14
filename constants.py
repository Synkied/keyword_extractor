from pdf.pdf_extraction import PDFExtractor


UNWANTED_CHARS_REGEX = '[.,-:;–\'’!?<>)(\][}{/*=\n•`&‘“”%]'

HANDLED_FILE_TYPES = {
    'pdf': PDFExtractor,
}
