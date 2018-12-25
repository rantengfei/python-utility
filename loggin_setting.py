"""
logging setting
"""

import logging.config
from config import LOG_FILE_H5 as LOG_FILE, ERROR_LOG_FILE_H5 as ERROR_LOG_FILE


standard_format = '[%(asctime)s] [%(levelname)s] [%(thread)d] [%(filename)s:%(lineno)d] [%(message)s]'

simple_format = '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(message)s]'


# log setting
def log_setting(LOG_FILE, ERROR_LOG_FILE):
    LOGGING_DIC = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': standard_format
            },
            'simple': {
                'format': simple_format
            },
        },
        'filters': {},
        'handlers': {
            # print to terminal
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            # save to file
            'default': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': LOG_FILE, # log file
                'maxBytes': 1024*1024*100,  # log size 10M
                'backupCount': 50,
                'encoding': 'utf-8',
            },
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': ERROR_LOG_FILE,
                'maxBytes': 1024 * 1024 * 100,
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf-8',
            },
        },
        'loggers': {
            '': {
                'handlers': ['default', 'error', 'console'],
                'level': 'DEBUG',
                'propagate': True,  # up level
            },
        },
    }
    return LOGGING_DIC


def load_logging_config():
    logging.config.dictConfig(log_setting(LOG_FILE, ERROR_LOG_FILE))
    logger = logging.getLogger(__name__)
    logger.info('Starting worker!')
    logger.error('Starting error!')

if __name__ == '__main__':
    load_logging_config()
