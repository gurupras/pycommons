import subprocess
import logging
import argparse
import re

import generic_logging
logger = logging.getLogger()

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
