import logging
import logging.config

_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,  # Required to keep gunicorn logger alive
    "formatters": {
        "standard": {
            "class": "logging.Formatter",
            "format": "[%(asctime)s] %(levelname)s - %(message)s",
            "datefmt": "%d/%b/%y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": "/home/tcarbone/website-api/logs/flask.log",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 4,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

logging.config.dictConfig(_logging_config)
