import re

from computational_law.inmate_parser.utils import resolve_line, stitching_lines


class InmateParser(object):

    def __init__(self, lst_lines):
        '''
        Parameter
        ---------
        lst_lines: list of strings
                   assumes the lines are of un-interrupted dialog

        Initializes
        ----------
        self.inmate: str (from title of transcript)
        self.text: str (the actual text)
        self.is_good: bool (is the filename indicative of a good file?)

        Note
        ----
        Suggested sequence of events
        ip = InmateParser(lst_lines)
        ip.run()
        '''
        self.lst_lines = lst_lines

    def resolve_lines(self):
        '''Label the parts of the line as having been said by the inmate or not.
        '''
        self.resolved_lines = []
        for line in self.lst_lines:
            self.resolved_lines.extend(resolve_line(line))

    def stitch_lines(self):
        '''Regroup the dialog that spans several lines. Retain the inmate ones.
        '''
        self.lines = stitching_lines(self.resolved_lines)
        self.inmate_lines = [text for text, inmate_filter
                             in self.lines if inmate_filter]

    def extract_inmate_participation(self):
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
    ip.resolve_lines()
    ip.stitch_lines()
    # or: ip.extract_inmate_participation()
