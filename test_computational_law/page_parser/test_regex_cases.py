from computational_law.page_parser.regex_cases import section_page

def test_section_page():
    # Case: with no space
    str_input = 'Proceedings...........................................33'
    assert section_page(str_input) == [('Proceedings', 33)]

    # Case: with a space before the number
    str_input = 'Proceedings........................................... 3'
    assert section_page(str_input) == [('Proceedings', 3)]

    # Case: with a space before/after
    str_input = 'Proceedings .......................................... 3'
    assert section_page(str_input) == [('Proceedings', 3)]

    # Case: several white space
    str_input = 'Decision...................................................  95'
    assert section_page(str_input) == [('Decision', 95)]

    # Case: with 2 words
    str_input = 'Case Factors ........................................10'
    assert section_page(str_input) == [('Case Factors', 10)]

    # Case: pre|post as a third word
    str_input = 'Pre Commitment Factors ..............................19'
    assert section_page(str_input) == [('Pre Commitment Factors', 19)]

    # Case: Pre-
    str_input = 'Pre-Commitment Factors....................................19'
    assert section_page(str_input) == [('Pre-Commitment Factors', 19)]
    # Case: a lot of pages
    str_input = ('Page Proceedings ..................................... 3'
                 ' Case Factors ........................................10'
                 ' Pre Commitment Factors ..............................19'
                 ' Post Commitment Factors .............................25'
                 ' Parole Plans ........................................46'
                 ' Closing Statements ..................................59'
                 ' Recess ..............................................64'
                 ' Decision ............................................65'
                 ' Adjournment .........................................87'
                 ' Transcriber Certification ...........................88')

    expected_out = [('Page Proceedings', 3), ('Case Factors', 10),
                    ('Pre Commitment Factors', 19),
                    ('Post Commitment Factors', 25), ('Parole Plans', 46),
                    ('Closing Statements', 59), ('Recess', 64),
                    ('Decision', 65), ('Adjournment', 87),
                    ('Transcriber Certification', 88)]
    assert section_page(str_input) == expected_out


if __name__ == '__main__':
    test_section_page()
