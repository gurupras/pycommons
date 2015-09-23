import logging

__LOGGING_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ]: %(message)s"
__FILE_FORMAT = "%(message)s"

def init(level, filename=None):
	if filename:
		logging.basicConfig(filename=filename, filemode='w', format=__FILE_FORMAT, level=level)
	else:
		logging.basicConfig(format=__LOGGING_FORMAT, level=level)
