# Inmate Parser

There are several people that participate in the hearing parole process (Presiding Commissioner, Deputy Commissioner, Inmate, Attorney for Inmate...). This section allows us to study only the inmate's part of the dialog.

### Aim
Taking in a list of clean lines, keep only what the inmate says, grouping the dialog that spans several lines.

Example: The original text below (which has been pre-processed)
```
￼￼￼PRESIDING COMMISSIONER ANDERSON: My name is Arthur Anderson, A-N-D-E-R-S-O-N, Commissioner.
DEPUTY COMMISSIONER TURNER: Terri Turner, T-U-R-N- E-R, Deputy Commissioner.
DEPUTY DISTRICT ATTORNEY ARMBRUSTER: Bill Armbruster, Deputy District Attorney from Kings County, A-R-M-B-R-U-S-T-E-R.
ATTORNEY BROSGART: Kate Brosgart, Counsel for Mr. Hillery.
INMATE HILLERY: Booker T. Hillery, Jr.
￼￼￼￼￼DEPUTY COMMISSIONER TURNER: CDC Number?
INMATE HILLERY: My CDC Number is A-32262.
DEPUTY COMMISSIONER TURNER: Spell your last name,
please.
INMATE HILLERY: My last name is H-I-L-L-E-R-Y. DEPUTY COMMISSIONER TURNER: Thank you.
INMATE MODESTO: Yes, and grandchildren and great-grandchildren that I suspect I have, because my son got married, and they miss me. They love me. And so I could go live with my Indian council if I’m let
￼￼￼loose. I’ve got big -- the Indians, they would care for me because I’m an elder. So I would like to go home.
```

is transformed to the following

```python
￼￼['Booker T. Hillery, Jr.',
￼￼￼￼'My CDC Number is A-32262.',
'My last name is H-I-L-L-E-R-Y.',
'Yes, and grandchildren and great-grandchildren that I suspect I have, because my son got married, and they miss me. They love me. And so I could go live with my Indian council if I’m let
￼￼￼loose. I’ve got big -- the Indians, they would care for me because I’m an elder. So I would like to go home.']
```

### How to use the InmateParser

```python
# Get the lines in the file (with some text clean).
pp = PageParser(filename)
pp.prepare_page_num_to_lines()
look_up_page = pp.page_to_clean_lines

# Retain all the lines.
all_lines = []
for page in sorted(look_up_page):
    all_lines.extend(look_up_page[page])

# Focus on the inmate participation
ip = InmateParser(all_lines)
ip.extract_inmate_participation()
```

### Limits
When the original text is difficult to parse for a human, the InmateParser will not be successful at making sense of the text. Below is an example of such a place.

```
PRESIDING COMMISSIONER LABAHN: Do you understand that your attorney will also be providing this Panel
When do you take INMATE MODESTO: At various times of the day.
You are? What are you
Morning or night? Pardon me?
Okay. Do you
information concerning any disabilities that she feels you have, correct?
INMATE MODESTO: Yes, sir.
```
