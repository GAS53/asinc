
from props import SERVER_LOG_PATH, CLIENT_LOG_PATH

server_log_config = {
    "version": 1,
    "formatters": {
        "standard": {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    "handlers": {
        'console': {
            "class": "logging.StreamHandler",
            "formatter": "standard",

            'stream'  : 'ext://sys.stdout',
        },



        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": f"{SERVER_LOG_PATH}",
            'maxBytes': 1024,
            'backupCount': 3,
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", 'console'],
            "level": "INFO",
            'propagate': False
        }
    },
}

client_log_config = {
"version": 1,
    "formatters": {
        "standard": {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    "handlers": {
        'console': {
            "class": "logging.StreamHandler",
            "formatter": "standard",

            'stream'  : 'ext://sys.stdout',
        },



        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": f"{CLIENT_LOG_PATH}",
            'maxBytes': 1024,
            'backupCount': 3,
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", 'console'],
            "level": "INFO",
            'propagate': False
        }
    },
}