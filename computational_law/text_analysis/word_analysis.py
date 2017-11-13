import spacy

from collections import defaultdict

nlp = spacy.load('en')

def get_spacy(text):
    return nlp(unicode(text))

def get_pos_json(spacy_text):
    pos_tok = set(tok.pos_ for tok in spacy_text)
    pos_dict = defaultdict(list)
    for tok in spacy_text:
        pos_dict[tok.pos_].append(tok.string.strip().lower())
    return pos_dict

def find_ngrams(input_list, n):
    '''http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
    '''
    return zip(*[input_list[i:] for i in range(n)])
