from computational_law.parser.helper_functions import resolve_line


def test_resolved_line():
    # Not inmate:
    line = u'DEPUTY COMMISSIONER TURNER: CDC Number?'
    expected_extracted_text = [(u'CDC Number?', False)]
    assert resolved_line(line) == expected_extracted_text

    # only inmate:
    line = u'INMATE HILLERY: My CDC Number is A-32262.'
    expected_extracted_text = [(u'My CDC Number is A-32262.', True)]
    assert resolved_line(line) == expected_extracted_text

    # starts inmate
    line = u'INMATE HILLERY: My last name is H-I-L-L-E-R-Y. DEPUTY COMMISSIONER TURNER: Thank you.'
    expected_extracted_text = [(u'My last name is H-I-L-L-E-R-Y. ', True),
                               (u'Thank you.', False)]
    assert resolved_line(line) == expected_extracted_text


    # starts with nothing
    line = u'questions, and then well move on. Can you see? INMATE HILLERY: Partially, I have glasses. PRESIDING COMMISSIONER ANDERSON: Oh.'
    expected_label = 'mid inmate'
    expected_extracted_text = [(u'questions, and then well move on. Can you see? ', None),
                               (u'Partially, I have glasses. ', True),
                               (u'Oh.', False)]
    assert resolved_line(line) == expected_extracted_text


    # end with inmate

    # several INMATE statements
    line = 'INMATE HILLERY: No, I work every day, so... PRESIDING COMMISSIONER ANDERSON: So, youre okay? INMATE HILLERY: Yes, sir.'
    expected_extracted_text = [(u'No, I work every day, so... ', True),
                               (u'So, youre okay? ', False),
                               (u'Yes, sir.', True)]
    assert resolved_line(line) == expected_extracted_text


    # no label
    line = u'breaks in terms of, if you need a break or anything to stand up and stretch or whatever, in terms of back problems or anything, let us know.'
    expected_extracted_text = [(u'breaks in terms of, if you need a break or anything to stand up and stretch or whatever, in terms of back problems or anything, let us know.', None)]
    assert resolved_line(line) == expected_extracted_text


if __name__ == '__main__':
    test_resolved_line()
