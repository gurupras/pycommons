import logging

__LOGGING_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ]: %(message)s"

def init(level):
	logging.basicConfig(format=__LOGGING_FORMAT, level=level)
