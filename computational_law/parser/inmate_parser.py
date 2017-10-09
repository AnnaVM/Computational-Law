import re

from helper_functions.clean_files import clean_file, make_pages, is_good_file
from helper_functions.clean_line import resolve_line
from helper_functions.stitch_lines import stitching_lines

class InmateParser(object):

    def __init__(self, filename):
        self.filename = filename
        m = re.search(r'[A-Z]\s?-?\d{5}', filename)
        self.inmate = m.group() if m else None
        with open(filename, 'r') as f:
            self.text = f.read()
        self.is_good = is_good_file(filename)

    def parole_result(self):
        results = {'ADVANCED', 'AFFIRMED', 'APPROVED', 'DENIED', 'GRANTED',
                   'PLANS', 'POSTPONED', 'REAFFIRMED','RESCINDED',
                   'STIPULATED', 'WAIVED'}
        pattern = r'(?:PAROLE|HEARING) (?!HEARING)(?:{})'.format(r'|'.join(results))
        result = re.search(pattern, self.text)
        if result:
            return result.group()
        self.prep_text()
        pages = reversed(self.pages)
        for page in list(pages)[:8]:
            in_page = re.search(r'postpone|waive|denied|reschedule', ' '.join(page))
            if in_page:
                return in_page.group()

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

    def save_to_file(self, out_filename):
        out = self.run()
        if out:
            with open(out_filename, 'w') as f:
                f.write('\n'.join(self.inmate_lines))

if __name__ == '__main__':
    ip = InmateParser('../../transcripts/2009/!A-32262.txt')
    ip.prep_text()
    ip.resolve_lines()
    ip.stitch_lines()
