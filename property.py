import os
import socket
from random import choice


HOST = socket.gethostname()
# PORT = 15658
PORT = choice([x for x in range(12000, 19000)])

SERVER_LOG_PATH = 'log/server.log'
CLIENT_LOG_PATH = 'log/client.log'

COUNT_DEQUE = 5

PATH_LOGGING_CALL_FUNC = os.getcwd()+'/log/calling_func.txt'
DB_PATH = os.getcwd()+'/db.sqllite'

term_or_file = 'file' # terminal or file

MY_NONE = 'не выбран'


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
            "handlers": ['console'], # "file",
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
            "handlers": ['console'], # "file",
            "level": "INFO",
            'propagate': False
        }
    },
}