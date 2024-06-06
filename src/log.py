import logging

def setUpLogging(loglevel):
    # Add custom "debug2" level
    logging.setLoggerClass(CustomLogger)
    logging.addLevelName(9, "DEBUG2")

    # Create our stream handler
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-4s %(levelname)-8s %(message)s')
    console.setFormatter(formatter)

    # Set up all the logging streams
    for logger in ['', 'ai', 'gui', 'reso', 'batt', 'gsrv', 'gcli']:
        logging.getLogger(logger).setLevel(loglevel)
        logging.getLogger(logger).addHandler(console)
        logging.getLogger(logger).propagate = False


class CustomLogger(logging.Logger):
    def debug2(self, msg):
        self.log(9, msg)
