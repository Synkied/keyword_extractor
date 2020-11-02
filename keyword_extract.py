import argparse
import os

import pdfplumber


class KeyWordExtractor():
    """
    A keyword extractor.
    """
    def pdf_extract(self, path):
        """
        Extracting text from pdfs in a directory
        :str:directory, path to a directory containing pdfs
        """

        # walk the given directory, to search for pdf files
        pdf_texts = []  # create an empty list, to store all pdfs texts

        if os.path.isfile(path):
            current_pdf_text = self.parse_pdf(path)

        if os.path.isdir(path):
            for directory_root, sub_directories, files in os.walk(path):
                for filepath in files:
                    if self.is_pdf(filepath):
                        # get pdf directory path
                        absolute_path = os.path.abspath(directory_root)
                        # get pdf path (directory + filename)
                        pdf_path = os.path.join(absolute_path, filepath)

                        # parse a pdf
                        current_pdf_text = self.parse_pdf(pdf_path)

        # add all texts to a final list
        pdf_texts.append(current_pdf_text)
        return pdf_texts

    def parse_pdf(self, pdf_path):
        current_pdf_text = {}  # create an empty dict, to store pdf text
        filename = os.path.split(pdf_path)[-1]

        with pdfplumber.open(pdf_path) as pdf:
            # create empty list to store all pages text
            current_pdf_text[filename] = []

            # for each page, append text to the list
            for page in pdf.pages:
                page_text = page.extract_text()
                # only add text if text on the page
                if page_text:
                    current_pdf_text[filename].append(page_text)

        return current_pdf_text

    def is_pdf(self, path):
        _, ext = os.path.splitext(path)

        # if not a pdf, ignore file
        if ext not in ['.pdf']:
            return False

        return True


if __name__ == '__main__':
    """
    Pass arguments in command line
    pdf_directory: path to a directory
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d')
    group.add_argument('-f')
    args = parser.parse_args()

    directory = args.d
    file = args.f

    kwext = KeyWordExtractor()
    if directory:
        pdf_texts = kwext.pdf_extract(directory)
    if file:
        pdf_texts = kwext.pdf_extract(file)