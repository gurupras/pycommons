import logging

_LOGGING_FORMAT = "[%(threadName)-10s  %(filename)s:%(lineno)s - %(funcName)-10s() ]: %(message)s"
_FILE_FORMAT = "[%(asctime)-16s]: %(message)s"

__INITIALIZED = False

class LoggingFormatter(logging.Formatter):
	fmt = "[%(threadName)-10s  %(filename)s:%(lineno)s - " + \
						"%(funcName)-10s() ]: %(message)s"

	def __init__(self, fmt=None, datefmt=None):
		if not fmt:
			fmt = LoggingFormatter.fmt
		super(LoggingFormatter, self).__init__(fmt, datefmt)

	def get_level_prefix(self, record):
		level_prefix = None
		if record.levelno is logging.WARNING:
			level_prefix = 'W'
		elif record.levelno is logging.ERROR:
			level_prefix = 'E'
		elif record.levelno is logging.CRITICAL:
			level_prefix = 'C'
		elif record.levelno is logging.DEBUG:
			level_prefix = 'D'
		elif record.levelno is logging.INFO:
			level_prefix = 'I'
		elif record.levelno is logging.NOTSET:
			level_prefix = 'V'
		else:
			level_prefix = 'CUSTOM'
		return level_prefix
	def format(self, record):
		level_prefix = self.get_level_prefix(record)

		record.msg = level_prefix + "/" + record.msg

		result = super(LoggingFormatter, self).format(record)
		return result


class Logger(object):
	pass

def init(level, filename=None, format=None):
	global __INITIALIZED
	if __INITIALIZED:
		return
	Logger.fmt = format if format is not None else _LOGGING_FORMAT
	Logger.level = level

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
			fmt = _FILE_FORMAT
		fileh = logging.FileHandler(filename, 'w')
		fileh.setFormatter(LoggingFormatter(fmt))
		logger.addHandler(fileh)
	# Add console handler
	consoleh = logging.StreamHandler()
	consoleh.setFormatter(LoggingFormatter())
	logger.addHandler(consoleh)
	__INITIALIZED = True

def add_file_handler(file, logger, format=None):
	handler = logging.FileHandler(file)
	handler.setLevel = Logger.level
	fmt = LoggingFormatter(format if format is not None else Logger.fmt)
	handler.setFormatter(fmt)
	logger.addHandler(handler)


def add_stream_handler(stream, logger, format=None):
	handler = logging.StreamHandler(stream)
	handler.setLevel = Logger.level
	fmt = LoggingFormatter(format if format is not None else Logger.fmt)
	handler.setFormatter(fmt)
	logger.addHandler(handler)
