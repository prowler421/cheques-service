import logging


def get_logger(logname, level=logging.INFO):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-12s %(funcName)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M',
                        filemode='a')

    # Now, define a couple of other loggers which might represent areas in your
    # application:
    logger = logging.getLogger(logname)

    return logger
