from computational_law.inmate_parser.utils import stitching_lines, resolve_line


def test_resolve_line():
    # Not inmate:
    line = u'DEPUTY COMMISSIONER TURNER: CDC Number?'
    expected_extracted_text = [(u'CDC Number?', False)]
    assert resolve_line(line) == expected_extracted_text

    # only inmate:
    line = u'INMATE HILLERY: My CDC Number is A-32262.'
    expected_extracted_text = [(u'My CDC Number is A-32262.', True)]
    assert resolve_line(line) == expected_extracted_text

    # starts inmate
    line = u'INMATE HILLERY: My last name is H-I-L-L-E-R-Y. DEPUTY COMMISSIONER TURNER: Thank you.'
    expected_extracted_text = [(u'My last name is H-I-L-L-E-R-Y. ', True),
                               (u'Thank you.', False)]
    assert resolve_line(line) == expected_extracted_text


    # starts with nothing
    line = u'questions, and then well move on. Can you see? INMATE HILLERY: Partially, I have glasses. PRESIDING COMMISSIONER ANDERSON: Oh.'
    expected_label = 'mid inmate'
    expected_extracted_text = [(u'questions, and then well move on. Can you see? ', None),
                               (u'Partially, I have glasses. ', True),
                               (u'Oh.', False)]
    assert resolve_line(line) == expected_extracted_text


    # end with inmate

    # several INMATE statements
    line = 'INMATE HILLERY: No, I work every day, so... PRESIDING COMMISSIONER ANDERSON: So, youre okay? INMATE HILLERY: Yes, sir.'
    expected_extracted_text = [(u'No, I work every day, so... ', True),
                               (u'So, youre okay? ', False),
                               (u'Yes, sir.', True)]
    assert resolve_line(line) == expected_extracted_text


    # no label
    line = u'breaks in terms of, if you need a break or anything to stand up and stretch or whatever, in terms of back problems or anything, let us know.'
    expected_extracted_text = [(u'breaks in terms of, if you need a break or anything to stand up and stretch or whatever, in terms of back problems or anything, let us know.', None)]
    assert resolve_line(line) == expected_extracted_text


def test_stitching_lines():
    lst = [('text 0', True),('text 1', None)]
    expected_out = [('text 0 text 1', True)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', True), ('text 1', None), ('text 2', False)]
    expected_out = [('text 0 text 1', True), ('text 2', False)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', True), ('text 1', False), ('text 2', False)]
    expected_out = [('text 0', True), ('text 1', False), ('text 2', False)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', True), ('text 1', False), ('text 2', True)]
    expected_out = [('text 0', True), ('text 1', False), ('text 2', True)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', False), ('text 1', None), ('text 2', False)]
    expected_out = [('text 0 text 1', False) , ('text 2', False)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', False), ('text 1', False), ('text 2', True)]
    expected_out = [('text 0', False), ('text 1', False), ('text 2', True)]
    assert stitching_lines(lst) == expected_out


    lst = [('text 0', False), ('text 1', False), ('text 2', False)]
    expected_out = [('text 0', False), ('text 1', False), ('text 2', False)]
    assert stitching_lines(lst) == expected_out

if __name__ == '__main__':
    test_resolve_line()
    test_stitching_lines()
