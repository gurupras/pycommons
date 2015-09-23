import logging

__LOGGING_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ]: %(message)s"
__FILE_FORMAT = "%(message)s"

def init(level, filename=None, format=None):
	logger = logging.getLogger()
	logger.setLevel(level)
	for handler in logger.handlers:
		logger.removeHandler(handler)

	# If format is set, use it for all streams
	fmt = None
	if format:
		fmt = format
	if filename:
		if not fmt:
			fmt = __FILE_FORMAT
		fileh = logging.FileHandler(filename, 'w')
		fileh.setFormatter(logging.Formatter(fmt))
		logger.addHandler(fileh)
	# Add console handler
	if not fmt:
		fmt = __LOGGING_FORMAT
	consoleh = logging.StreamHandler()
	consoleh.setFormatter(logging.Formatter(fmt))
	logger.addHandler(consoleh)
