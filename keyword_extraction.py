import argparse
import mimetypes
import os


from constants import HANDLED_FILE_TYPES


class KeyWordExtractor():
    """
    A keyword extractor.
    """
    def text_extract(self, path):
        """
        Extracting text from pdfs in a directory
        :str:directory, path to a directory containing pdfs
        """
        texts = {}

        if os.path.isdir(path):
            for directory_root, sub_directories, files in os.walk(path):
                for relative_filepath in files:
                    absolute_path = os.path.abspath(directory_root)
                    filepath = os.path.join(
                        absolute_path,
                        relative_filepath
                    )
                    file_type = self.determine_file_type(filepath)
                    texts.setdefault(file_type, {})

                    extracted_text = self.agg_datas(file_type, filepath)
                    filename = os.path.split(filepath)[-1]
                    texts[filename] = extracted_text

        elif os.path.isfile(path):
            filename = os.path.split(path)[-1]
            file_type = self.determine_file_type(path)
            extracted_text = self.agg_datas(file_type, path)
            texts[filename] = extracted_text

        print(texts)

        # walk the given directory, to search for pdf files

    def agg_datas(self, file_type, filepath):
        if file_type in HANDLED_FILE_TYPES.keys():
            handler = HANDLED_FILE_TYPES[file_type]()
            text = handler.extract_text(filepath)

            return text

    def determine_file_type(self, path):
        """
        Try guessing what's the file type
        """
        file_type_name = ''

        file_type, encoding = mimetypes.guess_type(path)
        if file_type:
            file_type_name = file_type.split('application/')[-1]

        print(path, file_type_name)

        return file_type_name


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
        kwext.text_extract(directory)
    if file:
        kwext.text_extract(file)
