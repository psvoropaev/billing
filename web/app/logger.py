import os

from logging.config import dictConfig
# from logstash_async.handler import AsynchronousLogstashHandler

from web.app import config


def create_logger():
    dictConfig({
        'version': 1,
        'formatters': {
            'basic': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'file': {
                'formatter': 'basic',
                'level': config.LOG_LEVEL,
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join('logs', 'app.log'),
                'when': 'midnight',
                'interval': 1,
                'backupCount': 10
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'stream': 'ext://sys.stdout'
            },
        },
        'loggers': {
            config.APP_NAME: {
                'handlers': ['console', 'file'],
                'level': config.LOG_LEVEL,
                'propagate': True,
            },
        },
        'disable_existing_loggers': False
    })
