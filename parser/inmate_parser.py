import re

from helper_functions.clean_files import clean_file, make_pages
from helper_functions.clean_line import resolve_line
from helper_functions.stitch_lines import stitching_lines

class InmateParser(object):

    def __init__(self, filename):
        self.filename = filename
        m = re.search(r'[A-Z]\s?-?\d{5}', filename)
        self.inmate = m.group() if m else None

    def prep_text(self):
        self.lst_lines = clean_file(self.filename)
        self.pages = make_pages(self.lst_lines)

    def resolve_lines(self):
        self.resolved_lines = []
        for page in self.pages[1:]:
            for line in page:
                self.resolved_lines.extend(resolve_line(line))

    def stitch_lines(self):
        self.lines = stitching_lines(self.resolved_lines)
        self.inmate_lines = [text for text, inmate_filter
                             in self.lines if inmate_filter]

    def run(self):
        self.prep_text()
        if self.pages == []:
            return None
        self.resolve_lines()
        self.stitch_lines()
        return self.inmate_lines


if __name__ == '__main__':
    ip = InmateParser('../../transcripts/2009/!A-32262.txt')
    ip.prep_text()
    ip.resolve_lines()
    ip.stitch_lines()
