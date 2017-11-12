# Page Parser

The Parole Hearing transcripts have a lot of structural elements. Here we will be making the most of the organisation in pages and of the presence of an index listing the various expected sections and the corresponding page number.

### Aim
Given a filename (`.txt`), have an easy access i) to the different pages, ii) to the different sections.

Example of the information contained in the index portion of the document. The first line is actually the page number.

```
￼￼￼￼￼￼2
INDEX
                                                    Page 
Proceedings ........................................ 3
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

## Dividing the content into pages
# Get the lines in the file (with some text clean).
lst_lines = clean_file(filename)

# Divide into pages.
page_to_lines = make_pages(lst_lines)

# Clean up some repeat lines, and remove line number.
page_to_clean_lines = clean_pages(page_to_lines)

## Identifying sections and their page numbers
# Identify the index.
lst_index_page = find_index_page(page_num_to_page)

# Make the sections
lst_sections = extract_section_information(lst_index_page)

# Allow to look the pages.
max_page = max(page_to_clean_lines.keys())
sections_to_page_nums = make_section_to_page_nums(section_information, max_page)
```
