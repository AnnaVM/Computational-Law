import re

def stitching_lines(lst_labeled_lines):
    if len(lst_labeled_lines) == 0:
        return None
    hold_label = None
    hold_text = ''
    lst = []
    for sub_text, sub_label in lst_labeled_lines:
        # print sub_text, sub_label
        if sub_label in [True, False]:
            # print 'if > ', sub_label, ' ({})'.format(sub_text)
            if hold_text != '':
                lst.append((hold_text, hold_label))
            hold_label = sub_label
            hold_text = sub_text
        elif sub_label is None:
            # print 'if > None'
            hold_text += ' ' + sub_text
        # print '{} | hold {} . {}'.format(lst, hold_text, hold_label)
    lst.append((hold_text, hold_label))
    return lst
