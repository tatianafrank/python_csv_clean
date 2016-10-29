#/usr/bin/python
# -*- coding: utf-8 -*-

"""
This script takes test.csv and normalizes text in the bio field to
space-delimited string, replaces state abbreviations in the state field 
with state names, validates the dates in start_date column and transforms 
them to ISO format. clean_file is called at the bottom with test.csv and 
solution.csv as arguments.
"""

import csv
import re
from dateutil.parser import parser, parse


def clean_file(r_file, w_file):
	"""Takes test.csv, cleans the Bio, State, and Start_date columns, 
	and writes normalized output to solution.csv

	"""
	test_csv = open(r_file, 'rb')
	solution_csv = open(w_file, 'w')
	reader = csv.reader(test_csv)
	writer = csv.writer(solution_csv)
	headers = next(reader, None)
	state_dict = create_state_dict();

	if headers:
		headers.append('start_date_description')
		writer.writerow(headers)

	for row in reader:
		# replace state abbrev with state name
		row[5] = state_name(row[5], state_dict)
		# normalize bio
		row[8] = strip_space(row[8])
		# convert date to ISO format if original date is a valid format
		if date_offset(row[10]):
			row[10] = parser().parse(row[10]).strftime('%Y-%m-%d')
		else:
			# append invalid date to adjacent column
			row = row[:11] + [row[10]]

		writer.writerow(row)

	test_csv.close()
	solution_csv.close()


def strip_space(str):
	"""Strip extra whitespace using regular expression."""
	str = str.strip()
	str = re.sub(r'\s+', ' ', str)
	return str


def state_name(state, state_dict):
	"""Return state name for given state abbreviation."""
	try: 
		s_dict = state_dict[state]
	except KeyError as err:
		s_dict = None
	return s_dict

def create_state_dict():
	with open('state_abbreviations.csv') as state_csv:
		reader = csv.reader(state_csv)
		s_dict = {rows[0]: rows[1] for rows in reader}
	return s_dict

def date_offset(date):
	"""Check for invalid date formats i.e missing year or random string."""
	date_attr = ("year", "day", "month")
	if parser()._parse(date)[0] is None:
		return False
	for attr in date_attr:
		if getattr(parser()._parse(date)[0], attr) is None:
			return False
	return True


clean_file('test.csv', 'solution.csv')
