import re

def resolve_line(line):
    '''Label parts of the line as having been said by the inmate or not.
    Parameter
    ---------
    line: str

    Returns
    -------
    list of tuples (str, bool or None)
    '''
    # Split the line along the fully capitalized words (usually indicates a new
    # person starting to speak)
    line = re.sub(r"[A-Z]'[A-Z]", '', line)
    lst = re.split(r'([A-Z][A-Z]+ [A-Z][A-Z]+(?: [A-Z][A-Z]+){0,5}):?\s?', line)

    # No information on the person speaking.
    if len(lst) == 1:
        return [(lst[0], None)]


    out = []
    keep_flag = True
    # The line starts with a person identified (INMATE : abcd...).
    if len(lst) > 1 and lst[0] == '':
        for label, text in zip(lst[1:], lst[2:]):
            if keep_flag:
                out.append((text, label[0:6] == 'INMATE'))
            keep_flag = not keep_flag
        return out

    # The line starts with plain text. (abcd...)
    if len(lst) > 1 and lst[0] != '':
        out.append((lst[0], None))
        for label, text in zip(lst[1:], lst[2:]):
            if keep_flag:
                out.append((text, label[0:6] == 'INMATE'))
            keep_flag = not keep_flag
        return out


def stitching_lines(lst_labeled_lines):
    '''Regroup dialog that spans several lines.
    Parameters
    ----------
    lst_labeled_lines: list of tuples (str, bool/None)

    Returns
    ------
    list
    '''
    if len(lst_labeled_lines) == 0:
        return None
    hold_label = None
    hold_text = ''
    lst = []
    for sub_text, sub_label in lst_labeled_lines:
        if sub_label in [True, False]:
            if hold_text != '':
                lst.append((hold_text, hold_label))
            hold_label = sub_label
            hold_text = sub_text
        elif sub_label is None:
            hold_text += ' ' + sub_text
    lst.append((hold_text, hold_label))
    return lst
