# Page Parser

### Goal
Format a filename (`.txt`) to have access i) to the different pages, ii) to have access the different sections.

```
￼￼￼￼￼￼2
INDEX
Page Proceedings ........................................ 3
Case Factors ....................................... 10
Pre-Commitment Factors ............................. 10
Post-Commitment Factors ............................ 11
Parole Plans ....................................... 23
Closing Statements ................................. 27
Recess ............................................. 29
Decision ........................................... 30
Adjournment ........................................ 39
Transcriber Certification .......................... 40
￼￼￼￼￼￼￼￼￼￼WPU, Inc.
```

### How to use the scripts

```python
# Get the lines in the file (with some text clean).
lst_lines = clean_file(filename)

# Divide into pages.
page_to_lines = make_pages(lst_lines)

# Clean up some repeat lines, and remove line number.
page_to_clean_lines = clean_pages(page_to_lines)

# Moving on to sections.
# Identify the index.
lst_index_page = find_index_page(page_num_to_page)

# Make the sections
lst_sections = extract_section_information(lst_index_page)

# Allow to look the pages.
max_page = max(page_to_clean_lines.keys())
sections_to_page_nums = make_section_to_page_nums(section_information, max_page)
```
