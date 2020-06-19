import logging.config
import sys

CONSOLE = 'console_logger'
DEBUG = 'debug_logger'
ERROR = 'error_logger'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # do not run debug logger in production
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'error_logfile': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],  # run logger in production
            'class': 'logging.FileHandler',
            'filename': 'error.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        CONSOLE: {
            'handlers': ['console'],
            'level': 'INFO'
        },
        DEBUG: {
            'handlers': ['debug_logfile'],
            'level': 'DEBUG'
        },
        ERROR: {
            'handlers': ['error_logfile'],
            'level': 'ERROR'
        },
    },
    'root': {
        "level": "INFO",
        "handlers": ["console", "debug_logfile"]
    }
}


def logger():  # (log_type=CONSOLE):
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger()  # (log_type)
    return log
