''' Основные переменные для сервера '''

import os


MAX_CLIENTS = 5

SERVER_LOG_PATH = 'log/server.log'

DB_SERVER = os.getcwd()+'/Server/db_server.sqllite'


term_or_file = 'file' # terminal or file

MY_NONE = 'не выбран'

AUTH_KEY = b'my_key_authasdfghjkl'
SALT = b'my _salt'

server_log_config2 = {
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

server_log_config1 = {
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