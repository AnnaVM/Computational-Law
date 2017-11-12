import re

REG = re.compile(r'(?P<section>(?:Pre |Post |Pre-|Post-)?\w+(?: \w+)?) ?\.+ *(?P<page>\d+)')

def section_page(str_input, reg=REG):
    return list((m.group('section'), int(m.group('page')))
                for m in reg.finditer(str_input))
