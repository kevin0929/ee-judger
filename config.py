import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simpleFormatter": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",   # emit to sys.stderr(default)
            "level": "DEBUG",
            "formatter": "simpleFormatter",
            "stream": "ext://sys.stdout"
        },
        "fileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simpleFormatter",     # debug.log's type mapping to formatters
            "filename": "debug.log",
            "maxBytes": 5000000,
            "backupCount": 5,
            "encoding": "utf8"
        }
    },
    "loggers": {
        "": {
            "handlers": ["consoleHandler", "fileHandler"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

logging.config.dictConfig(config=LOGGING_CONFIG)
logger = logging.getLogger()