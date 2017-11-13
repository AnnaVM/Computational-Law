# Text Analysis

Investigating the vocabulary/word choices in the inmate's part of the dialog.

### Aim

**Approaches:**
- `pos`: investigating different parts of speech (verbs, nouns, adjectives...)
- `n-grams`: get a sense of the n-grams used by inmates.


**Different pre-processing options:**
- using raw text, splitting on new lines and white spaces.
- using Spacy tokenization (removing punctuation)
- using Spacy tokenization (removing punctuation and stopwords)
- using Spacy tokenization and lemmatization

### How to use the scripts


```python

## Prepare the list
filename = './transcripts/2009/!A-32914.txt'
# Create the page look up dictionary.
pp = PageParser(filename)
pp.prepare_page_num_to_lines()
look_up_page = pp.page_to_clean_lines

all_lines = []
for page in sorted(look_up_page):
    all_lines.extend(look_up_page[page])

# Keep the inmate's portion.
ip = InmateParser(all_lines)
inmate_dialog = ip.extract_inmate_participation()

## Studying the text
wa = WordAnalysis(inmate_dialog)

# One of the options: looking at bigrams, with stopwords removed
wa.make_n_gram_list(n=2, clean_up_options='spacy_words_no_stop')
```
