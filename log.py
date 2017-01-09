import logging


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(handler)

    return logger

# LOGGER_NAME = 'browserentropy'
# logger = get_logger(name=LOGGER_NAME, level=logging.INFO)
