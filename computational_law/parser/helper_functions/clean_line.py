import re

def resolve_line(line):
    line = re.sub(r"[A-Z]'[A-Z]", '', line)
    lst = re.split(r'([A-Z][A-Z]+ [A-Z][A-Z]+(?: [A-Z][A-Z]+){0,5}):?\s?', line)
    if len(lst) == 1:
        return [(lst[0], None)]
    out = []
    keep_flag = True
    if len(lst) > 1 and lst[0] == '':
        for label, text in zip(lst[1:], lst[2:]):
            if keep_flag:
                out.append((text, label[0:6] == 'INMATE'))
            keep_flag = not keep_flag
        return out
    if len(lst) > 1 and lst[0] != '':
        out.append((lst[0], None))
        for label, text in zip(lst[1:], lst[2:]):
            if keep_flag:
                out.append((text, label[0:6] == 'INMATE'))
            keep_flag = not keep_flag
        return out
