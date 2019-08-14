import logging

def setupLogger():
    logger = logging.getLogger(__package__)
    
    # Levels are as follows:
    '''
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
    '''
    LEVEL  = logging.DEBUG
    FILE   = "debug.log"
    FORMAT = "[%(levelname)8s]:%(filename)-23s#%(lineno)-3s --- %(message)s"
    # FORMAT =  "%(lineno)s:\n%(message)s"  # the old format

    handler = logging.FileHandler(FILE)
    handler.setFormatter(logging.Formatter(FORMAT))
    logger.setLevel(LEVEL)

    logger.addHandler(handler)