import os

import pdfplumber


class PDFExtractor():
    """
    A PDF text extractor.
    """
    def extract_text(self, filepath):
        """
        Extracting text from pdfs in a directory
        :str:filepath, path to a pdf file
        """
        current_pdf_text = self.parse_pdf(filepath)

        return current_pdf_text

    def parse_pdf(self, pdf_path):
        current_pdf_text = {}  # create an empty dict, to store pdf text

        with pdfplumber.open(pdf_path) as pdf:
            # create empty list to store all pages text

            # for each page, append text to the list
            for page in pdf.pages:
                page_number = 'page_%s' % (page.page_number)
                current_pdf_text.setdefault(page_number, {})
                page_text = page.extract_text()
                # only add text if text on the page
                if page_text:
                    current_pdf_text[page_number] = page_text

        return current_pdf_text

    def is_pdf(self, path):
        _, ext = os.path.splitext(path)

        # if not a pdf, ignore file
        if ext not in ['.pdf']:
            return False

        return True
