import os
import re

def get_files(folder_path):

	file_paths = []
	for root, dirs, files in os.walk(folder_path):
		for filename in files:
			if is_good_file(filename):
				file_paths.append(os.path.join(root,filename))
	return file_paths

def is_good_file(filename):
	filename_filters = ['Advisory', 'board', 'Commissioner', 'Committee',
						 'Expedite', 'memo', 'public'] #Not case sensitive
	if filename.endswith(".txt"):
		for filter_string in filename_filters:
			if filter_string.lower() in filename.lower():
				return False
	return True

def clean_file(filename):
	lst_lines = []
	with open(filename, 'r') as f:
		raw_text = f.read()
		raw_text = raw_text.replace('\xbc', '')\
						   .replace('\xef', '')\
						   .replace('\xbf', '')\
						   .replace('\xe2\x80\x99', '')\
						   .replace('\xe2\x80\x9c', '')\
						   .replace('\xe2\x80\x9d', '')

		for line in re.split(r'(?:\r|\n)', raw_text):
			lst_lines.append(line)
	return lst_lines


def make_pages(lst_lines):
	pages, page = [], []
	for line in lst_lines:
	    m = re.match(r'\d+$', line)
	    only_num = re.match(r'\d\s[\d\s]+$', line)
	    line = re.sub(r'[^a-z]+DECISION PAGE[^a-z]+', r'', line)
	    # 14 understanding that your client, inmate Rushing, wishes
	    line = re.sub(r'^\d\d?\s', '', line)
	    if only_num or line == 'WPU, Inc.' or line == '':
	        continue
	    if m and page != []:
	        pages.append(page)
	        page = []
	    elif m is None:
	        page.append(line)
	return pages
