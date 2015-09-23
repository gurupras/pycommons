import logging

__LOGGING_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ]: %(message)s"
__FILE_FORMAT = "%(message)s"

def init(level, filename=None):
	logger = logging.getLogger()
	logger.setLevel(level)
	for handler in logger.handlers:
		logger.removeHandler(handler)
	if filename:
		fileh = logging.FileHandler(filename, 'w')
		fileh.setFormatter(logging.Formatter(__FILE_FORMAT))
		logger.addHandler(fileh)
	# Add console handler
	consoleh = logging.StreamHandler()
	consoleh.setFormatter(logging.Formatter(__LOGGING_FORMAT))
	logger.addHandler(consoleh)
