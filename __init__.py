import os
import sys
import datetime
import subprocess
import logging
import argparse
import re

import gzip

import generic_logging
logger = logging.getLogger()

import pool

def f_to_c(f):
	celsius = (f - 32) * (5/9.)
	return celsius

def c_to_f(c):
	fahrenheit = ((c * (9/5.)) + 32)
	return fahrenheit

def open_file(fpath, mode, gz=False):
	name, ext = os.path.splitext(fpath)
	if ext == '.gz' or gz is True:
		return gzip.open(fpath, mode)
	return open(fpath, mode)

def run(cmd,
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		log=False, fail_on_error=True):
	logger.info('$ ' + cmd)
	p = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)

	stdout = []
	stderr = []
	if log:
		while True:
			nextline = p.stdout.readline().strip()
			if nextline == '' and p.poll() != None:
				break
			logger.info(nextline)
			stdout.append(nextline)
			try:
				nextline = p.stderr.readline().strip()
				if nextline == '' and p.poll() != None:
					break
				logger.error(nextline)
				stderr.append(nextline)
			except:
				pass

	p.wait()
	if not log:
		stdout.append('\n'.join(p.stdout.readlines()))
		if p.stderr:
			stderr.append('\n'.join(p.stderr.readlines()))
	if p.returncode != 0:
		logger.warning('Process returned: %d' % (p.returncode))
		if fail_on_error:
			raise Exception('%s: %d' % (cmd, p.returncode))
	return p.returncode, '\n'.join(stdout), '\n'.join(stderr)

class ListAction(argparse.Action):
	def __call__(self, parser, args, values, option_string=None) :
		range_re = re.compile('range\\((?P<start>\\d+),(?P<end>\\d+),(?P<increment>\\d+)\\)')
		values = values.replace(' ', '')
		m = range_re.match(values)
		if m:
			start = int(m.group('start'))
			end   = int(m.group('end'))
			incr  = int(m.group('increment'))
			values = ['%d' % (i) for i in range(start, end, incr)]
			values = ','.join(values)
		values = values.split(",")
		setattr(args, self.dest, values)

class DateRangeAction(argparse.Action):
	def __call__(self, parser, args, values, option_string=None) :
		patterns = [
			re.compile('(?P<start>\d{2}/\d{2}/\d{4})\s*(-)?\s*(?P<end>\d{2}/\d{2}/\d{4})'),
			re.compile('(?P<start>\d{8})\s*(-)?\s*(?P<end>\d{8})')
		]
		dt_patterns = [
			'%m/%d/%Y',
			'%Y%m%d'
		]
		values = values.replace(' ', '')
		for idx, p in enumerate(patterns):
			m = p.match(values)
			if m:
				start = datetime.datetime.strptime(m.group('start'), dt_patterns[idx])
				end = datetime.datetime.strptime(m.group('end'), dt_patterns[idx])
				days = (end - start).days
				assert days >= 0, 'End date cannot be before start date!'

				values = []
				for d in range(days):
					values.append(start + datetime.timedelta(days=d))
				break
		setattr(args, self.dest, values)

class SizeAction(argparse.Action):
	SIZE_DICT = {
		'b' : 1,
		'k' : 1024,
		'm' : 1024*1024,
		'g' : 1024*1024*1024,
	}

	def __call__(self, parser, args, values, option_string=None) :
		pattern = re.compile(r'(?P<size>\d+)(?P<unit>[bBkKmMgG])')
		m = pattern.match(values)
		if not m:
			raise Exception("'%s' does not satisfy pattern '%s'" % (values, pattern.pattern))
		size = int(m.group('size'))
		for k, v in SizeAction.SIZE_DICT.iteritems():
			if m.group('unit').lower() == k:
				size *= v
		setattr(args, self.dest, size)

class LoggingLevelAction(argparse.Action):
	def __call__(self, parser, args, values, option_string=None) :
		try:
			level = getattr(logging, values)
		except:
			level = logging.DEBUG
		setattr(args, self.dest, level)


# Taken from http://stackoverflow.com/a/613218/1761555
def sort_dict(d, pos=0, key=None):
	import operator
	lambdafn = None
	if not key:
		lambdafn = operator.itemgetter(pos)
	else:
		lambdafn = lambda x: key(x[pos])
	sorted_tuples = sorted(d.items(), key=lambdafn)
	return sorted_tuples

# Taken from http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def print_progress(iterations, total, prefix = '', suffix = '', decimals = 2, barLength = 80, colors=False):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iterations  - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : Number of decimal places to display
		barLength   - Optional  : Number of characters that encompass bar length
		colors      - Optional  : Specifies whether to use ANSI terminal colors
	"""
	COLOR_RED = '\033[31m'
	COLOR_GREEN = '\033[32m'
	COLOR_YELLOW = '\033[33m'
	COLOR_ENDC = '\033[0m'
	filledLength    = int(round(barLength * iterations / float(total)))
	percents        = round(100.00 * (iterations / float(total)), decimals)
	bar             = '#' * filledLength + '-' * (barLength - filledLength)

	color = ''
	if colors:
		if percents < 30:
			color = COLOR_RED
		elif percents < 70:
			color = COLOR_YELLOW
		else:
			color = COLOR_GREEN
	string = '%s%s [%s] %s%s %s\r' % (color, prefix, bar, percents, '%', suffix)
	sys.stderr.write(string)
	sys.stderr.write(COLOR_ENDC)
	sys.stderr.flush()
	if iterations == total:
		sys.stderr.write("\n")
		sys.stderr.flush()

