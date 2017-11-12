import re

from collections import Counter, defaultdict

from computational_law.page_parser.regex_cases import section_page

def clean_file(filename):
    '''
    Parameters
    ----------
    filename: str
    
    Returns
    -------
    list of string
    '''
	lst_lines = []
	with open(filename, 'r') as f:
		raw_text = f.read()
		raw_text = raw_text.replace('\xbc', '')\
						   .replace('\xef', '')\
						   .replace('\xbf', '')\
						   .replace('\xe2\x80\x99', "'")\
						   .replace('\xe2\x80\x9c', '"')\
						   .replace('\xe2\x80\x9d', '"')

		for line in re.split(r'(?:\r|\n)', raw_text):
			lst_lines.append(line)
	return lst_lines


def make_pages(lst_lines):
    '''Break the file into pages.
    Parameters
    ----------
    lst_lines: list of strings
            basically the lines of the files, with weird characters removed

    Returns
    -------
    dictionary
            page_number (int): list of lines (list of strings)
    '''
    num_lines = len(lst_lines)
    page_to_lines = defaultdict(list)
    for i, line in enumerate(lst_lines):
        num_current_line = re.match(r'^\d+$', line)
        if num_current_line:
            print num_current_line.group()
            break
    else:
        print 'no pages made'
        return {}
    page = int(num_current_line.group())
    for i, line in enumerate(lst_lines):
        num_current_line = re.match(r'^\d+$', line)
        if (num_current_line
                and int(num_current_line.group()) == page
                and i + 1 < num_lines):
            # Check that this is a real page number, and not just
            # an enumeration ['10', '11', '12', '13', ...]
            next_line = lst_lines[i + 1]
            num_next_line = re.match(r'^\d+$', next_line)
            if num_next_line:
                continue
            # Good chance it's a real page number
            first_page = False
            page += 1
        else:
            page_to_lines[page - 1].append(line)
    return page_to_lines


def clean_pages(page_to_lines):
    '''Remove any line that appears a suspiscous amount of times. Remove line
    numbers.
    Parameters
    ----------
    dictionary
            page_number (int): list of lines (list of strings)
    Returns
    -------
    dictionary
            same structure as input

    Example
    -------
    - some numbers
    '1 2 3 4 5 6 7 8 9'
    '10'
    - some short phrases
    'Northern California Court Reporters'
    - numbered lines:
     '1 P ROCEEDINGS',
     "2 PRESIDING COMMISSIONER DOYLE: Okay. The time's",
     '3 about 1:30. This is a Subsequent Parole Consideration',
     '4 Hearing for Maurice Nicholas, right?',
     '5 INMATE NICHOLAS: Nicholas.',
     '6 PRESIDING COMMISSIONER DOYLE: CDC Number',
     "7 A-91933. Today's date is February 4th of 2009. We're",
     '8 located at CMC. Mr. Nicholas was received on April 17th',
     '9 of 1973 from Los Angeles County. The controlling offense',

    Note
    ----
    We do not want to remove somewhat frequent occurences like 'Yes, Sir'
    or 'No, Sir'
    '''
    # Figure out which are the most commonly used phrases.
    page_line = []
    for lst in page_to_lines.values():
        page_line.extend(lst)
    phrase_value_pairs = filter(lambda x: x[1] > len(page_to_lines) - 10 and x[1] > 3,
                                Counter(page_line).most_common())
    # Remove common phrases.
    phrases = set([phrase for phrase, _ in phrase_value_pairs])
    page_to_clean_lines = {}
    for page_num, lines in page_to_lines.iteritems():
        page_to_clean_lines[page_num] = filter(lambda line: line not in phrases,
                                               lines)
    # Remove line number for lines that are numbered in the beginning.
    # NOTE(AnnaVM) this is an inelegant approach, try checking that the lines
    # before and after are also numbered.
    for page, lst_lines in page_to_clean_lines.iteritems():
        clean_lst_lines = [re.sub(r'^([1-3]?[0-9] ?)', '', line) for line in lst_lines]
        page_to_clean_lines[page] = clean_lst_lines
    return page_to_clean_lines


def find_index_page(page_num_to_page):
    '''Identify the index page.
    Parameters
    ----------
    page_num_to_page: dictionary
                    page_number (as int): lines (list of strings)

    Returns
    -------
    list of strings (the lines of the INDEX)

    Note
    ----
    Some variability: the index can appear on page 1 or 2.
    '''
    # Usually it's on the second page
    best_guess = 2
    lst_index_page = page_num_to_page.get(best_guess, [])
    if (len(lst_index_page) >= 2
         and 'index' in lst_index_page[0].replace(' ', '').lower()):
        print 'index on page 2'
        return lst_index_page

    # it might be in the first page
    for page_num in [0, 1]:
        lst_index_page = page_num_to_page.get(page_num, [])
        if lst_index_page and 'ii INDEX' in lst_index_page or 'INDEX' in lst_index_page:
            print 'index on first page'
            try:
                i = lst_index_page.index('ii INDEX')
            except:
                i = lst_index_page.index('INDEX')
            j = i + 10
            return lst_index_page[i:j+1]

    return []

def extract_section_information(lst_index_page):
    '''Given the list of lines on the index page, link the section to its page.
    Parameters
    ----------
    lst_index_page: list of strings

    Returns
    -------
    list of tuples (string, int)

    Example
    -------
    [('Page Proceedings', 3),
     ('Case Factors', 27),
     ('Pre-Commitment Factors', 18),
     ('Post-Commitment Factors', 42),
     ('Parole Plans', 56),
     ('Closing Statements', 66),
     ('Recess', 80),
     ('Decision', 81),
     ('Adjournment', 96),
     ('Transcript Certification', 98)]
    '''
    if not lst_index_page:
        return [], ''
    lst_sections = []
    # 2 items: typically ['INDEX', 'text of interest']
    # sometime 3 items ['INDEX', 'text of interest', 'footer]
    if len(lst_index_page) <= 3:
        lst_sections = section_page(lst_index_page[1])
    # For longer lists, typically, each line of interest is an item in the list
    elif len(lst_index_page) > 3:
        str_input = ' '.join(lst_index_page[1:])
        lst_sections = section_page(str_input)

    return lst_sections


def make_section_to_page_nums(section_information, max_page):
    '''Maps sections to the page range they are located at.

    Parameters
    ----------
    section_information: list of tuples (str, int)
    max_pages: int

    Returns
    -------
    dictionary
        key (as str: the section name),
        value (as tuple of int, the pages corresponding to the section)

    Example
    -------
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

    make_section_to_page_nums(section_information, max_page=99)
    {'Adjournment': (96, 97),
     'Case Factors': (27, 17),
     'Closing Statements': (66, 79),
     'Decision': (81, 95),
     'Parole Plans': (56, 65),
     'Post-Commitment Factors': (42, 55),
     'Pre-Commitment Factors': (18, 41),
     'Proceedings': (3, 26),
     'Recess': (80, 80),
     'Transcript Certification': (98, 99)}
    '''
    if not section_information:
        return {}
    sections_to_page_nums = {}
    # Initialize the name_ and page_ parameters.
    name_, page_ = section_information[0]
    # Fix the first section name when necessary.
    name_ = 'Proceedings' if 'Page ' in name_ else name_
    for name, page in section_information[1:]:
        sections_to_page_nums[name_] = (page_, page - 1)
        name_, page_  = name, page
    # Get the last section.
    sections_to_page_nums[name_] = (page_, max_page)

    return sections_to_page_nums
