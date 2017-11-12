from computational_law.parser.helper_functions.regex_cases import section_page

# Index like sections and how they are parsed

# Case Normal: 3 items
normal = ['INDEX',
          'Page Proceedings ........................................... 3 Case Factors ........................................10 Pre Commitment Factors ..............................19 Post Commitment Factors .............................25 Parole Plans ........................................46 Closing Statements ..................................59 Recess ..............................................64 Decision ............................................65 Adjournment .........................................87 Transcriber Certification ...........................88',
          'WPU, Inc.']

# Case weird index
normal = ['INDE X',
           'Page Proceedings ........................................... 3 Case Factors ........................................10 Pre Commitment Factors ..............................19 Post Commitment Factors .............................25 Parole Plans ........................................46 Closing Statements ..................................59 Recess ..............................................64 Decision ............................................65 Adjournment .........................................87 Transcriber Certification ...........................88',
           'WPU, Inc.']

def find_index_page(page_num_to_page):
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


def prep_section(lst_index_page):
    if not lst_index_page:
        return [], ''
    lst_sections = []
    footer = ''
    # 3 items: typically ['INDEX', 'text of interest', 'footer']
    if len(lst_index_page) <= 3:
        lst_sections = section_page(lst_index_page[1])
        footer = lst_index_page[2] if len(lst_index_page) == 3 else ''
    # typically, each line of interest is an item in the list
    elif len(lst_index_page) > 3:
        str_input = ' '.join(lst_index_page[1:])
        lst_sections = section_page(str_input)

    return lst_sections, footer
