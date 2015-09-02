import logging

__LOGGING_FORMAT = "[%(filename)20s:%(lineno)s - %(funcName)20s() ]: %(message)s"
logging.basicConfig(format=__LOGGING_FORMAT)
