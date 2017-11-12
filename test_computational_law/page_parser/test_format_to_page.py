from computational_law.page_parser.format_to_page import (make_pages,
                                                          clean_pages,
                                                          find_index_page,
                                                          extract_section_information,
                                                          make_section_to_page_nums)


def test_make_pages():
    # Case: no page number
    lst_lines = ['no number',
                 'Still no number!']
    assert make_pages(lst_lines) == {}

    # Case: first page number given is 2
    lst_lines = ['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA',
                 'BOARD OF PAROLE HEARINGS',
                 'In the matter of the Life Term Parole Consideration )',
                 'Hearing of: MARVIN MUTCH',
                 '2',
                 'INDEX',
                 'Page Proceedings......................................... 3',
                 'Northern California Court Reporters',
                 '3',
                 'PROCEEDINGS',
                 'DEPUTY COMMISSIONER MAHONEY: On the record.']
    expected_out = {1: ['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA',
                        'BOARD OF PAROLE HEARINGS',
                        'In the matter of the Life Term Parole Consideration )',
                        'Hearing of: MARVIN MUTCH'],
                    2: ['INDEX',
                        'Page Proceedings......................................... 3',
                        'Northern California Court Reporters'],
                    3: ['PROCEEDINGS',
                        'DEPUTY COMMISSIONER MAHONEY: On the record.']}
    assert make_pages(lst_lines) == expected_out

    # Case: first page number given is 1
    lst_lines = ['SUBSEQUENT PAROLE CONSIDERATION HEARING',
                 '          STATE OF CALIFORNIA',
                 '       BOARD OF PAROLE HEARINGS',
                 'In the matter of the Life )',
                 'OTHERS PRESENT:',
                 'ii',
                 'INDEX',
                 '                                                        Page',
                 'Proceedings................................................1',
                 'Case Factors...............................................5',
                 'Pre-Commitment Factors.....................................7',
                 '--oOo--',
                 '1',
                 '1 P ROCEEDINGS',
                 "2 PRESIDING COMMISSIONER DOYLE: Okay. The time's",
                 '3 about 1:30. This is a Subsequent Parole Consideration',
                 '4 Hearing for Maurice Nicholas, right?']

    expected_out = {0: ['SUBSEQUENT PAROLE CONSIDERATION HEARING',
                        '          STATE OF CALIFORNIA',
                        '       BOARD OF PAROLE HEARINGS',
                        'In the matter of the Life )',
                        'OTHERS PRESENT:',
                        'ii',
                        'INDEX',
                        '                                                        Page',
                        'Proceedings................................................1',
                        'Case Factors...............................................5',
                        'Pre-Commitment Factors.....................................7',
                        '--oOo--'],
                    1: ['1 P ROCEEDINGS',
                        "2 PRESIDING COMMISSIONER DOYLE: Okay. The time's",
                        '3 about 1:30. This is a Subsequent Parole Consideration',
                        '4 Hearing for Maurice Nicholas, right?']}
    assert make_pages(lst_lines) == expected_out

    # Case: do not pick up unwanted numbers.
    lst_lines = ['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA',
                 'BOARD OF PAROLE HEARINGS',
                 'In the matter of the Life Term Parole Consideration )',
                 'Hearing of: MARVIN MUTCH',
                 '8',
                 'INDEX',
                 'Page Proceedings......................................... 3',
                 'Northern California Court Reporters',
                 '9',
                 'PROCEEDINGS',
                 'DEPUTY COMMISSIONER MAHONEY: On the record.'
                 '1 2 3 4 5 6 7 8 9',
                 '10',
                 '11',
                 '12',
                 '13',
                 '14',
                 '15',
                 '16',
                 '17',
                 '18',
                 '19',
                 '20',
                 '21',
                 '22',
                 '23',
                 '24',
                 '25',
                 'Northern California Court Reporters',
                 '4',
                 "Mr. Mutch. It's S-N-E-D-E-K-E-R.",
                 'INMATE MUTCH: Marvin Mutch, M-U-T-C-H, B, as in',
                 'baker, 65921.',
                 'PRESIDING COMMISSIONER ANDERSON: Thank you. Let',
                 "the record reflect we have two officers for security only and we're going to -- Mr. Mutch, we're going to go over some ADA issues, American with Disabilities. What I have in front of me is a BPH 1073. You signed this Form on 8/30/2013. You have a physical disability and what is that?",
                 'INMATE MUTCH: I have a drop foot from a stroke. PRESIDING COMMISSIONER ANDERSON: Okay.',
                 'INMATE MUTCH: So I wear a brace and use a cane. PRESIDING COMMISSIONER ANDERSON: Okay. And you',
                 'wear your glasses. I see you have your glasses here today.',
                 'INMATE MUTCH: Yes, sir.']
    expected_out = {7: ['SUBSEQUENT PAROLE CONSIDERATION HEARING STATE OF CALIFORNIA',
                        'BOARD OF PAROLE HEARINGS',
                        'In the matter of the Life Term Parole Consideration )',
                        'Hearing of: MARVIN MUTCH'],
                    8: ['INDEX',
                        'Page Proceedings......................................... 3',
                        'Northern California Court Reporters'],
                    9: ['PROCEEDINGS',
                        'DEPUTY COMMISSIONER MAHONEY: On the record.1 2 3 4 5 6 7 8 9',
                        '11',
                        '12',
                        '13',
                        '14',
                        '15',
                        '16',
                        '17',
                        '18',
                        '19',
                        '20',
                        '21',
                        '22',
                        '23',
                        '24',
                        '25',
                        'Northern California Court Reporters',
                        '4',
                        "Mr. Mutch. It's S-N-E-D-E-K-E-R.",
                        'INMATE MUTCH: Marvin Mutch, M-U-T-C-H, B, as in',
                        'baker, 65921.',
                        'PRESIDING COMMISSIONER ANDERSON: Thank you. Let',
                        "the record reflect we have two officers for security only and we're going to -- Mr. Mutch, we're going to go over some ADA issues, American with Disabilities. What I have in front of me is a BPH 1073. You signed this Form on 8/30/2013. You have a physical disability and what is that?",
                        'INMATE MUTCH: I have a drop foot from a stroke. PRESIDING COMMISSIONER ANDERSON: Okay.',
                        'INMATE MUTCH: So I wear a brace and use a cane. PRESIDING COMMISSIONER ANDERSON: Okay. And you',
                        'wear your glasses. I see you have your glasses here today.',
                        'INMATE MUTCH: Yes, sir.']}
    assert make_pages(lst_lines) == expected_out


def test_clean_pages():
    # Case: repeated short phrase (here: 'Capitol Electronic Reporting')
    page_to_lines = {1: ['Hi', 'Capitol Electronic Reporting'],
                     2: ['This is a test.', 'Capitol Electronic Reporting'],
                     3: ['So let us start.', 'Capitol Electronic Reporting'],
                     4: ['a', 'Capitol Electronic Reporting'],
                     5: ['b', 'Capitol Electronic Reporting'],
                     6: ['c', 'Capitol Electronic Reporting'],
                     7: ['d', 'Capitol Electronic Reporting'],
                     8: ['e', 'Capitol Electronic Reporting'],
                     9: ['f', 'Capitol Electronic Reporting'],
                     10: ['g', 'Capitol Electronic Reporting'],
                     11: ['h', 'Capitol Electronic Reporting'],
                     12: ['i', 'Capitol Electronic Reporting'],
                     13: ['j', 'Capitol Electronic Reporting']}
    expected_out = {1: ['Hi'],
                    2: ['This is a test.'],
                    3: ['So let us start.'],
                    4: ['a'],
                    5: ['b'],
                    6: ['c'],
                    7: ['d'],
                    8: ['e'],
                    9: ['f'],
                    10: ['g'],
                    11: ['h'],
                    12: ['i'],
                    13: ['j']}
    assert clean_pages(page_to_lines) == expected_out

    # Case: Several page numbers on their own and the phrase
    page_to_lines = {1: ['Hi', 'Capitol Electronic Reporting'],
                     2: ['This is a test.', 'Capitol Electronic Reporting'],
                     3: ['So let us start.', 'Capitol Electronic Reporting'],
                     4: ['1', '2', '3', 'a'],
                     5: ['1', '2', '3', 'b', 'Capitol Electronic Reporting'],
                     6: ['c', 'Capitol Electronic Reporting'],
                     7: ['d', 'Capitol Electronic Reporting'],
                     8: ['1', '2', '3','e', 'Capitol Electronic Reporting'],
                     9: ['1', '2', '3', 'f', 'Capitol Electronic Reporting'],
                     10: ['1', '2', '3', 'hi', 'Capitol Electronic Reporting'],
                     11: ['1', '2', '3', 'h', 'Capitol Electronic Reporting'],
                     12: ['1', '2', '3', 'i', 'Capitol Electronic Reporting'],
                     13: ['1', '2', '3', 'j', 'Capitol Electronic Reporting']}
    expected_out = {1: ['Hi'],
                    2: ['This is a test.'],
                    3: ['So let us start.'],
                    4: ['a'],
                    5: ['b'],
                    6: ['c'],
                    7: ['d'],
                    8: ['e'],
                    9: ['f'],
                    10: ['hi'],
                    11: ['h'],
                    12: ['i'],
                    13: ['j']}
    assert clean_pages(page_to_lines) == expected_out

    # Case: remove the line number from the beginning of the line.
    page_to_lines = {1: ['1 P ROCEEDINGS',
                         "2 PRESIDING COMMISSIONER DOYLE: Okay. The time's",
                         '3 about 1:30. This is a Subsequent Parole Consideration',
                         '4 Hearing for Maurice Nicholas, right?',
                         '5 INMATE NICHOLAS: Nicholas.',
                         '6 PRESIDING COMMISSIONER DOYLE: CDC Number',
                         "7 A-91933. Today's date is February 4th of 2009. We're",
                         '8 located at CMC. Mr. Nicholas was received on April 17th',
                         '9 of 1973 from Los Angeles County. The controlling offense',
                         '10 for which he was committed is Murder in the First Degree,',
                         '11 Case A291331. One count of 187, additional counts of']}
    expected_out = {1: ['P ROCEEDINGS',
                        "PRESIDING COMMISSIONER DOYLE: Okay. The time's",
                        'about 1:30. This is a Subsequent Parole Consideration',
                        'Hearing for Maurice Nicholas, right?',
                        'INMATE NICHOLAS: Nicholas.',
                        'PRESIDING COMMISSIONER DOYLE: CDC Number',
                        "A-91933. Today's date is February 4th of 2009. We're",
                        'located at CMC. Mr. Nicholas was received on April 17th',
                        'of 1973 from Los Angeles County. The controlling offense',
                        'for which he was committed is Murder in the First Degree,',
                        'Case A291331. One count of 187, additional counts of']}
    assert clean_pages(page_to_lines) == expected_out

def test_find_index_page():
    # Case: On page zero
    page_num_to_page = {0: ['SUBSEQUENT PAROLE CONSIDERATION HEARING',
                            'PANEL PRESENT:',
                            'ii',
                            'INDEX',
                            'Proceedings.................................1',
                            'Case Factors.................................5',
                            'Recess.................................91',
                            '--oOo--'],
                        1: ['1 P ROCEEDINGS',
                            "2 PRESIDING COMMISSIONER DOYLE: Okay. The time's",
                            '3 about 1:30. This is a Subsequent Parole Consideration',
                            '4 Hearing for Maurice Nicholas, right?',
                            '5 INMATE NICHOLAS: Nicholas.',
                            '6 PRESIDING COMMISSIONER DOYLE: CDC Number']}
    expected_out = ['INDEX',
                    'Proceedings.................................1',
                    'Case Factors.................................5',
                    'Recess.................................91',
                    '--oOo--']
    assert find_index_page(page_num_to_page) == expected_out

    # Case: on the second page
    page_num_to_page = {1: ['LAWRENCE MODESTO ) _________ )',
                            "CALIFORNIA MEN'S COLONY SAN LUIS OBISPO, CALIFORNIA DECEMBER 9, 2009 11:50 A.M.",
                            'PANEL PRESENT:',
                            'PETER LABAHN, Presiding Commissioner RANDY KEVORKIAN, Deputy Commissioner',
                            'Elizabeth A. Scott, TypeToo Transcription & Billing'],
                        2: ['INDEX',
                            '     Page',
                            'Proceedings...............................17',
                            'Pre-Commitment Factors....................27',
                            'Post-Commitment Factors...................31',
                            'Parole Plans..............................42']}
    expected_out = ['INDEX',
                    '     Page',
                    'Proceedings...............................17',
                    'Pre-Commitment Factors....................27',
                    'Post-Commitment Factors...................31',
                    'Parole Plans..............................42']
    assert find_index_page(page_num_to_page) == expected_out

    # Case: on page zero, INDEX is not in its own line
    page_num_to_page = {0: ['SUBSEQUENT PAROLE CONSIDERATION HEARING',
                            'PANEL PRESENT:',
                            'ii INDEX',
                            'Proceedings.................................1',
                            'Case Factors.................................5',
                            'Recess.................................91',
                            '--oOo--'],
                        1: ['1 P ROCEEDINGS',
                            "2 PRESIDING COMMISSIONER DOYLE: Okay. The time's",
                            '3 about 1:30. This is a Subsequent Parole Consideration',
                            '4 Hearing for Maurice Nicholas, right?',
                            '5 INMATE NICHOLAS: Nicholas.',
                            '6 PRESIDING COMMISSIONER DOYLE: CDC Number']}
    expected_out = ['ii INDEX',
                    'Proceedings.................................1',
                    'Case Factors.................................5',
                    'Recess.................................91',
                    '--oOo--']
    assert find_index_page(page_num_to_page) == expected_out

    # Case: variations in the way INDEX is spelled
    page_num_to_page = {1: ['LAWRENCE MODESTO ) _________ )',
                            "CALIFORNIA MEN'S COLONY SAN LUIS OBISPO, CALIFORNIA DECEMBER 9, 2009 11:50 A.M.",
                            'PANEL PRESENT:',
                            'PETER LABAHN, Presiding Commissioner RANDY KEVORKIAN, Deputy Commissioner',
                            'Elizabeth A. Scott, TypeToo Transcription & Billing'],
                        2: ['I NDEX',
                            '     Page',
                            'Proceedings...............................17',
                            'Pre-Commitment Factors....................27',
                            'Post-Commitment Factors...................31',
                            'Parole Plans..............................42']}
    expected_out = ['I NDEX',
                    '     Page',
                    'Proceedings...............................17',
                    'Pre-Commitment Factors....................27',
                    'Post-Commitment Factors...................31',
                    'Parole Plans..............................42']
    assert find_index_page(page_num_to_page) == expected_out


def test_extract_section_information():
    # Case
    lst_index_page = []
    assert extract_section_information(lst_index_page) == ([], '')

    # Case: Each on 1 line
    lst_index_page = ['I NDEX',
                      '     Page',
                      'Proceedings...............................17',
                      'Pre-Commitment Factors....................27',
                      'Post-Commitment Factors...................31',
                      'Parole Plans..............................42']
    expected_out = [('Page Proceedings', 17),
                    ('Pre-Commitment Factors', 27),
                    ('Post-Commitment Factors', 31),
                    ('Parole Plans', 42)]
    assert extract_section_information(lst_index_page) == expected_out

    # Case: 3 or less lines
    lst_index_page = ['I NDEX',
                      ('     Page Proceedings...............................17 '
                       'Pre-Commitment Factors....................27'
                       'Post-Commitment Factors...................31'
                       'Parole Plans..............................42')]
    expected_out = [('Page Proceedings', 17),
                    ('Pre-Commitment Factors', 27),
                    ('Post-Commitment Factors', 31),
                    ('Parole Plans', 42)]
    assert extract_section_information(lst_index_page) == expected_out


def test_make_section_to_page_nums():
    # Case:
    section_information = [
                         ('Page Proceedings', 3),
                         ('Case Factors', 27),
                         ('Pre-Commitment Factors', 18),
                         ('Post-Commitment Factors', 42),
                         ('Parole Plans', 56),
                         ('Closing Statements', 66),
                         ('Recess', 80),
                         ('Decision', 81),
                         ('Adjournment', 96),
                         ('Transcript Certification', 98)]
    expected_out = {'Adjournment': (96, 97),
                    'Case Factors': (27, 17),
                    'Closing Statements': (66, 79),
                    'Decision': (81, 95),
                    'Parole Plans': (56, 65),
                    'Post-Commitment Factors': (42, 55),
                    'Pre-Commitment Factors': (18, 41),
                    'Proceedings': (3, 26),
                    'Recess': (80, 80),
                    'Transcript Certification': (98, 99)}
    assert make_section_to_page_nums(section_information, max_page=99) == expected_out

if __name__ == '__main__':
    test_make_pages()
    test_clean_pages()
    test_find_index_page()
    test_extract_section_information()
    test_make_section_to_page_nums()
