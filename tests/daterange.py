import unittest
import datetime
import itertools
import argparse
import shlex
import pycommons

class TestDateRange(unittest.TestCase):

	def setUp(self):
		parser = argparse.ArgumentParser()
		parser.add_argument('dates', action=pycommons.DateRangeAction)
		self.parser = parser

	def test_slash_pattern(self):
		dr = '"04/25/2016 - 05/03/2016"'
		cmdline = 'dummyprog ' + dr
		cmdline = shlex.split(cmdline)
		args = self.parser.parse_args(cmdline[1:])

		dates = args.dates

		start = datetime.datetime(2016, 04, 25)
		end = datetime.datetime(2016, 05, 03)
		expected = []
		for x in range((end - start).days):
			expected.append(start + datetime.timedelta(days=x))
		assert all([x == y for x, y in itertools.izip(dates, expected)])

	def test_yyyymmdd(self):
		dr = '"20160425 - 20160503"'
		cmdline = 'dummyprog ' + dr
		cmdline = shlex.split(cmdline)
		args = self.parser.parse_args(cmdline[1:])

		dates = args.dates

		start = datetime.datetime(2016, 04, 25)
		end = datetime.datetime(2016, 05, 03)
		expected = []
		for x in range((end - start).days):
			expected.append(start + datetime.timedelta(days=x))
		assert all([x == y for x, y in itertools.izip(dates, expected)])

	@unittest.expectedFailure
	def test_negative(self):
		# Negative test
		dr = '"05/03/2016 - 04/25/2016"'
		cmdline = 'dummyprog ' + dr
		cmdline = shlex.split(cmdline)
		args = self.parser.parse_args(cmdline[1:])



if __name__ == '__main__':
	unittest.main()
