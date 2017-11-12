from computational_law.text_analysis.helper_functions.word_analysis import get_spacy, find_ngrams, get_pos_json

def test_get_pos_json():
    text = u'This is a sentence to tag as best as possible.'
    spacy_text = get_spacy(text)
    assert get_pos_json(spacy_text) == {u'ADV': [u'as ', u'best '], u'NOUN': [u'sentence ', u'tag '], u'ADP': [u'to ', u'as '], u'DET': [u'This ', u'a '], u'PUNCT': [u'.'], u'VERB': [u'is '], u'ADJ': [u'possible']}

def test_find_ngrams():
    input_lst = ['This', 'is', 'a', 'sentence', 'to', 'make', 'n-grams', '.']
    assert find_ngrams(input_lst, 1) == [('This',), ('is',), ('a',), ('sentence',), ('to',), ('make',), ('n-grams',), ('.',)]

    assert find_ngrams(input_lst, 2) == [('This', 'is'), ('is', 'a'), ('a', 'sentence'), ('sentence', 'to'), ('to', 'make'), ('make', 'n-grams'), ('n-grams', '.')]

    assert find_ngrams(input_lst, 3) == [('This', 'is', 'a'), ('is', 'a', 'sentence'), ('a', 'sentence', 'to'), ('sentence', 'to', 'make'), ('to', 'make', 'n-grams'), ('make', 'n-grams', '.')]

if __name__ == '__main__':
    test_get_pos_json()
    test_find_ngrams()
