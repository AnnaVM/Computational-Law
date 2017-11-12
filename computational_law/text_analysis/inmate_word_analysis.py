import os
import re

from collections import defaultdict, Counter
from computational_law.text_analysis.word_analysis import get_spacy, get_pos_json, find_ngrams


class WordAnalysis(object):

    def __init__(self, lst_dialog=None, filename=None):
        '''
        Parameters
        ----------
        lst_dialog: list of strings/unicode
        filename: str
                  input file, with the list of strings

        Initializes
        -----------
        self.lst_dialog: list of strings/unicode
        self.text: str/unicode

        Notes
        -----
        Suggested sequence of events
        wa = WordAnalysis(lst_dialog) or WordAnalysis(filename)
        wa.make_pos_json()
        wa.make_n_gram_list(2)
        '''
        self.lst_dialog = lst_dialog if lst_dialog is not None else []
        if filename:
            with open(filename, 'r') as f:
                self.text = f.read()
                self.lst_dialog = re.split(r'\n', self.text)
        else:
            self.text = '\n'.join(lst_dialog)

    def make_spacy_text(self):

        self.spacy_text = get_spacy(self.text.decode('utf-8'))
        return self.spacy_text

    def make_pos_json(self):
        self.pos_json = get_pos_json(self.make_spacy_text())
        return self.pos_json

    def make_n_gram_list(self, n=2, clean_up_options=None):
        '''
        Parameters
        ----------
        n: int
           n in n gram
        clean_up_options: None, 'spacy_words', 'lemma'
        '''
        if clean_up_options == None:
            input_list = re.split(r'\n|\s+', self.text)
        elif clean_up_options == 'spacy_words':
            input_list = [tk.text.strip() for tk in self.make_spacy_text()
                          if not tk.is_punct and tk.text.strip()]
        elif clean_up_options == 'spacy_words_no_stop':
            input_list = [tk.text.strip() for tk in self.make_spacy_text()
                          if not tk.is_punct and not tk.is_stop and tk.text.strip()]
        elif clean_up_options == 'lemma':
            input_list = [tk.lemma_.strip() for tk in self.make_spacy_text()]
        return find_ngrams(input_list, n=n)


def make_overall_pos_json(clean_directory):
    filenames  = os.listdir(clean_directory)
    full_filenames = [os.path.join(clean_directory, filename)
                      for filename in filenames]
    overall_pos_json = defaultdict(list)
    for i, filename in full_filenames:
        if i%100 == 0:
            print i
        wa = WordAnalysis(filename=filename)
        pos_json = wa.make_pos_json()
        for pos, lst_words in pos_json.iteritems():
            overall_pos_json[pos].extend(lst_words)
    return overall_pos_json


def make_overall_ngram_json(clean_directory, n=2, clean_up_options=None):
    filenames  = os.listdir(clean_directory)
    full_filenames = [os.path.join(clean_directory, filename)
                      for filename in filenames]
    overall_ngram_json = defaultdict(list)
    for i, filename in full_filenames:
        if i%100 == 0:
            print i
        wa = WordAnalysis(filename=filename)
        ngram_json = wa.make_n_gram_list(n=n, clean_up_options=clean_up_options)
        for pos, lst_words in ngram_json.iteritems():
            overall_ngram_json[pos].extend(lst_words)
    return overall_ngram_json
