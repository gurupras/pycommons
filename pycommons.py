import subprocess
import logging

import generic_logging
logger = logging.getLogger()

def run(cmd,
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
		log=False, fail_on_error=True):
	logger.info('$ ' + cmd)
	p = subprocess.Popen(cmd, shell=True, stdout=stdout, stderr=stderr)
	p.wait()

	stdout, stderr = p.communicate()
	if log:
		logger.debug(stdout)
		logger.warning(stderr)

	if p.returncode != 0:
		logger.warning('Process returned: %d' % (p.returncode))
		if fail_on_error:
			raise Exception('%s: %d' % (cmd, p.returncode))
	return p.returncode, stdout, stderr

