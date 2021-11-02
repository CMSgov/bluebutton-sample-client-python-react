import logging
import logging.config 
import os


# create class to allow for instantiation of different loggers within separate files
# within the appliation

class LoggerFactory(object):
    _LOG = logging.getLogger(__name__)

    @staticmethod
    def _create_logger(log_file, log_level):
        """
        A private method that interacts with the python logging module
        """
        main_base = os.path.dirname(os.path.dirname(__file__))
        #logging.getLogger('LoggerFactory').error('MAIN:'+main_base)
        config_file = os.path.join(main_base,'configs','logging.conf')
        #logging.getLogger('LoggerFactory').error('CONFIG:'+config_file)

        if not os.path.exists(config_file):
            msg = 'configuartion file does not exist!', config_file
            logging.getLogger('LoggerFactory').error(msg)
            raise ValueError(msg)

        # set the logging format and a few other settings
        logging.config.fileConfig(config_file)
        
        # Initialize class variable with logger object
        LoggerFactory._LOG = logging.getLogger(log_file)

        # set the logging level based on the user selection
        if log_level == "INFO":
            LoggerFactory._LOG.setLevel(logging.INFO)
        elif log_level == "ERROR":
            LoggerFactory._LOG.setLevel(logging.ERROR)
        elif log_level == "DEBUG":
            LoggerFactory._LOG.setLevel(logging.DEBUG)
        elif log_level == "WARNING":
            LoggerFactory._LOG.setLevel(logging.WARNING)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_file, log_level):
        """
        A static method called by other modules to initialize logger
        in their own module
        """
        logger = LoggerFactory._create_logger(log_file, log_level)

        # return the logger object
        return logger

    