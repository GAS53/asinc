
server_log_config = {
    "version": 1,
    "formatters": {
        "my_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "my_formatter",
            "filename": "server.log"
        },
    },
    "loggers": {
        "server": {
            "handlers": ["file_handler"],
            "level": "INFO",
        }
    },
}

client_log_config = {
    "version": 1,
    "formatters": {
        "my_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "my_formatter",
            "filename": "client.log"
        },
    },
    "loggers": {
        "client": {
            "handlers": ["file_handler"],
            "level": "INFO",
        }
    },
}