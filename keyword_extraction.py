import argparse
import mimetypes
import os
import re

from constants import HANDLED_FILE_TYPES
from constants import UNWANTED_CHARS_REGEX

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class KeyWordExtractor():
    """
    A keyword extractor.
    """

    def __init__(self, path, language):
        texts_agg = self.text_extract(path)
        self.lang_stopwords = []
        try:
            self.lang_stopwords = stopwords.words(language)
        except OSError:
            self.lang_stopwords = []

        self.text_words_count = self.keyword_extract(texts_agg)
        result = self.keywords_analyze(self.text_words_count)

        self.notable_keywords = result['notable_keywords']
        print(self)

    def __repr__(self):
        return 'Notable keywords: %s' % (self.notable_keywords)

    def text_extract(self, path):
        """
        Extracting text from pdfs in a directory
        :str:directory, path to a directory containing pdfs
        """

        texts_agg = {}

        if os.path.isdir(path):
            for directory_root, sub_directories, files in os.walk(path):
                for relative_filepath in files:
                    absolute_path = os.path.abspath(directory_root)
                    filepath = os.path.join(
                        absolute_path,
                        relative_filepath
                    )
                    file_type = self.determine_file_type(filepath)
                    texts_agg.setdefault(file_type, {})

                    extracted_text = self.agg_datas(file_type, filepath)
                    filename = os.path.split(filepath)[-1]
                    texts_agg[filename] = extracted_text

        elif os.path.isfile(path):
            filename = os.path.split(path)[-1]
            file_type = self.determine_file_type(path)
            extracted_text = self.agg_datas(file_type, path)
            texts_agg[filename] = extracted_text

        return texts_agg

    def keyword_extract(self, texts_agg):
        text_words_count = {}

        for f in texts_agg:
            text_words_count[f] = {}
            for page in texts_agg[f]:
                text_words_count[f][page] = {}
                page_text = self.clean_text(texts_agg[f][page])
                page_word_count = self.word_counter(page_text)

                text_words_count[f][page] = page_word_count

        return text_words_count

    def keywords_analyze(self, keywords_extract):
        notable_keywords = {}
        words = {}
        per_page_notable_keywords = {}
        means = []

        for f in keywords_extract:
            per_page_notable_keywords[f] = {}
            for page in keywords_extract[f]:
                per_page_notable_keywords[f][page] = {}
                page_words = keywords_extract[f][page]
                counters = page_words.values()
                page_max_counter = max(counters)
                page_min_counter = min(counters)
                page_mean = (page_max_counter + page_min_counter) / 2
                means.append(page_mean)

                for k, v in page_words.items():
                    if k not in words.keys():
                        words[k] = v
                    else:
                        words[k] += v

                    if v > page_mean:
                        per_page_notable_keywords[f][page][k] = v

        total_max = max(means)
        total_min = min(means)
        total_mean = (total_max + total_min) / 2

        for k, v in words.items():
            if v > total_mean:
                notable_keywords[k] = v

        sorted_notable_keywords = {
            k: v for k, v in sorted(
                notable_keywords.items(),
                key=lambda item: item[1],
                reverse=True
            )
        }

        result = {
            'notable_keywords': sorted_notable_keywords,
            'per_page_notable_keywords': per_page_notable_keywords,
        }
        return result

    def clean_text(self, text):
        text = re.sub(UNWANTED_CHARS_REGEX, ' ', text)
        words = word_tokenize(text)
        result = ' '.join(
            [
                word for word in words
                if word.lower() not in self.lang_stopwords
            ]
        )
        return result

    def word_counter(self, text):
        words_count = {}
        for word in word_tokenize(text):
            word = word.lower()
            if word not in words_count.keys():
                words_count[word] = 1
            else:
                words_count[word] += 1

        return words_count

    def agg_datas(self, file_type, filepath):
        if file_type in HANDLED_FILE_TYPES.keys():
            handler = HANDLED_FILE_TYPES[file_type]()
            text = handler.extract_text(filepath)

            return text

        return {}

    def determine_file_type(self, path):
        """
        Try guessing what's the file type
        """
        file_type_name = ''

        file_type, encoding = mimetypes.guess_type(path)
        if file_type:
            file_type_name = file_type.split('application/')[-1]

        return file_type_name


if __name__ == '__main__':
    """
    Pass arguments in command line
    pdf_directory: path to a directory
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', default="english")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d')
    group.add_argument('-f')
    args = parser.parse_args()

    path = ''
    language = args.l

    if args.d:
        path = args.d
    if args.f:
        path = args.f

    kwext = KeyWordExtractor(path, language)
