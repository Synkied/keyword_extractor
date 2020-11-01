import argparse
import os

import pdfplumber


def pdf_extract(pdfs_directory):
    """
    Extracting text from pdfs in a directory
    :str:pdfs_directory, path to a directory containing pdfs
    """

    # walk the given pdfs_directory, to search for pdf files
    pdfs_texts = []  # create an empty list, to store all pdfs texts
    for directory_root, sub_directories, files in os.walk(pdfs_directory):

        # for each pdf in the directory
        for filepath in files:
            current_pdf_text = {}  # create an empty dict, to store pdf text

            # get file extension
            _, ext = os.path.splitext(filepath)

            # if not a pdf, ignore file
            if ext not in ['.pdf']:
                continue

            # get pdf directory path
            absolute_path = os.path.abspath(directory_root)
            # get pdf path (directory + filename)
            pdf_path = os.path.join(absolute_path, filepath)

            # parse a pdf
            with pdfplumber.open(pdf_path) as pdf:
                # create empty list to store all pages text
                current_pdf_text[filepath] = []

                # for each page, append text to the list
                for page in pdf.pages:
                    page_text = page.extract_text()
                    # only add text if text on the page
                    if page_text:
                        current_pdf_text[filepath].append(page_text)

            # add all texts to a final list
            pdfs_texts.append(current_pdf_text)

    # print all pdfs texts, only to see it working
    print(pdfs_texts)


if __name__ == '__main__':
    """
    Pass arguments in command line
    pdf_directory: path to a directory
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('pdfs_directory')
    args = parser.parse_args()

    pdfs_directory = args.pdfs_directory
    pdf_extract(pdfs_directory)
