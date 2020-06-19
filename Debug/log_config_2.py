#  @Project SmartAlarm
#  @Copyright (c) 2019 AIPower. All Rights Reserved.

import logging.config
import os
import sys

from config.django_settings import BASE_DIR

_LOG_DIR = os.path.join(
    BASE_DIR,
    'logs',
)
os.makedirs(_LOG_DIR, exist_ok=True)

_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,

    # format in which logs will be written
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },

    # handlers define the file to be written, which level to write in that file,
    # which format to use and which filter applies to that logger
    'handlers': {
        'console_simple': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'console_verbose': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'debug_logfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(_LOG_DIR, 'debug.log'),
            'encoding': 'utf-8',
            'when': 'midnight',
            'interval': 1,
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'info_logfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(_LOG_DIR, 'info.log'),
            'encoding': 'utf-8',
            'when': 'midnight',
            'interval': 1,
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'error_logfile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(_LOG_DIR, 'error.log'),
            'encoding': 'utf-8',
            'when': 'midnight',
            'interval': 1,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },

    # here the handlers for the loggers and the level of each logger is defined
    'loggers': {
        'smart_alarm': {
            'handlers': ['console_simple', 'debug_logfile', ],
            'level': 'DEBUG',
        }
    },
}

logging.config.dictConfig(_LOG_CONFIG)

log = logging.getLogger('smart_alarm')
