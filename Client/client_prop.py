import os


CLIENT_LOG_PATH = 'log/client.log'

DB_CLIENT = os.getcwd()+'/db_client.sqllite'

term_or_file = 'file' # terminal or file

MY_NONE = 'не выбран'

AUTH_KEY = b'my_key_auth'


client_log_config2 = {
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

client_log_config1 = {
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