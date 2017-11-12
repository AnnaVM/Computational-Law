import re

from collections import Counter, defaultdict

from computational_law.parser.helper_functions.regex_cases import section_page


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


def clean_page(page_to_lines):
    '''Remove any line that appears a suspiscous amount of times.
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
    '''
    page_line = []
    for lst in page_to_lines.values():
        page_line.extend(lst)
    phrase_value_pairs = filter(lambda x: x[1] > len(page_to_lines) - 10,
                                Counter(page_line).most_common())

    phrases = set([phrase for phrase, _ in phrase_value_pairs])
    page_to_clean_lines = {}
    for page_num, lines in page_to_lines.iteritems():
        page_to_clean_lines[page_num] = filter(lambda line: line not in phrases,
                                               lines)
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
    lst_index_page = page_num_to_page.get(1, [])
    if lst_index_page and 'ii INDEX' in lst_index_page or 'INDEX' in lst_index_page:
        print 'index on page 1'
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


def make_section_to_page_num(section_information, page_to_lines):
    '''
    Parameters
    ----------
    section_information: list of tuple
    page_to_lines: dictionary

    Returns
    -------

    '''
    if not section_information:
        return {}
    sections_to_page_nums, sections_to_pages = {}, {}

    name_, page_ = section_information[0]
    for name, page in section_information[1:]:
        sections_to_page_nums[name_] = (page_, page - 1)
        name_, page_  = name, page
    sections_to_page_nums[name_] = (page_, max(page_to_lines.keys()) + 1)
    return sections_to_page_nums
    for section, (start, end) in sections_to_page_nums.iteritems():
        lst_lines = []
        for num in range(start, end + 1):
            if num in page_to_lines:
                lst_lines.extend(page_to_lines[num])
        sections_to_pages[section] = lst_lines
    return sections_to_pages
