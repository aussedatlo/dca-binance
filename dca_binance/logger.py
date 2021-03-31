import logging
import logging.handlers

__author__ = "Louis Aussedat"
__copyright__ = "Copyright (c) 2021 Louis Aussedat"
__license__ = "GPLv3"

def setup_logger(name, level):
    logFormatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-6s %(message)s")
    rootLogger = logging.getLogger()

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    log = logging.getLogger(name)
    log.setLevel(level)

    return log

def setup_logger_filename(name, path):
    rootLogger = logging.getLogger()
    logFormatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-6s %(message)s")

    fileHandler = logging.handlers.TimedRotatingFileHandler(
        "{0}/{1}.log".format(path, "dca-binance"), when='D', interval=31)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
