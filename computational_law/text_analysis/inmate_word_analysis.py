import os
import re

from collections import defaultdict, Counter
from helper_functions.word_analysis import get_spacy, get_pos_json, find_ngrams


class WordAnalysis(object):

    def __init__(self, lst_dialog=None, filename=None):
        self.lst_dialog = lst_dialog
        if filename:
            with open(filename, 'r') as f:
                self.text = f.read()
                self.lst_dialog = re.split(r'\n', self.text)
        else:
            self.text = '\n'.join(lst_dialog)

    def make_spacy_text(self):
        self.spacy_text = get_spacy(self.text)
        return self.spacy_text

    def make_pos_json(self):
        self.pos_json = get_pos_json(self.make_spacy_text())
        return self.pos_json

    def make_n_gram_list(self, n=2, clean_up_options=None):
        if clean_up_options == None:
            input_list = re.split(r'\n|\s+', self.text)
        return find_ngrams(input_list, n=2)


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
