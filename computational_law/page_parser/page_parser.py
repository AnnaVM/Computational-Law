import re

from computational_law.page_parser.format_to_page import (make_pages,
                                                          clean_file,
                                                          clean_pages,
                                                          find_index_page,
                                                          extract_section_information,
                                                          make_section_to_page_nums)


class PageParser(object):

    def __init__(self, filename):
        '''
        Parameter
        ---------
        filename: str
                  full path of a '.txt' file

        Initializes
        ----------
        self.inmate: str (from title of transcript)
        self.text: str (the actual text)
        self.is_good: bool (is the filename indicative of a good file?)

        Note
        ----
        Suggested sequence of events
        ip = InmateParser(input_filename)
        ip.parole_result()
        ip.run()  or  ip.save_to_file(output_filename)
        '''
        self.filename = filename
        m = re.search(r'[A-Z]\s?-?\d{5}', filename)
        self.inmate = m.group() if m else None
        with open(filename, 'r') as f:
            self.text = f.read()
        self.is_good = is_good_file(filename)

    def prepare_page_num_to_lines(self, clean_option=True):
        ## Dividing the content into pages
        # Get the lines in the file (with some text clean).
        self.lst_lines = clean_file(self.filename)

        # Divide into pages.
        self.page_to_lines = make_pages(self.lst_lines)

        if clean_option:
            # Clean up some repeat lines, and remove line number.
            self.page_to_clean_lines = clean_pages(self.page_to_lines)

    def prepare_sections(self, clean_option=True):
        page_num_to_page = self.page_to_clean_lines if clean_option else self.page_to_lines
        ## Identifying sections and their page numbers
        # Identify the index.
        lst_index_page = find_index_page(page_num_to_page)
        # Make the sections
        lst_sections = extract_section_information(lst_index_page)
        # Allow to look up the pages.
        max_page = max(page_num_to_page.keys())
        self.sections_to_page_nums = make_section_to_page_nums(lst_sections, max_page)

def is_good_file(filename):
	filename_filters = ['Advisory', 'board', 'Commissioner', 'Committee',
						 'Expedite', 'memo', 'public'] #Not case sensitive
	if filename.endswith(".txt"):
		for filter_string in filename_filters:
			if filter_string.lower() in filename.lower():
				return False
		return True
	return False
