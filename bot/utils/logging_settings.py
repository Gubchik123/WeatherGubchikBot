logger_config = {
    "version": 1,
    "formatters": {
        "my_formatter": {
            "format": "%(name)s: [%(filename)s - %(lineno)d] #%(levelname)-8s (%(asctime)s) %(message)s"
        }
    },
    "handlers": {
        "info_handler": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "my_formatter",
        },
        "error_handler": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "my_formatter",
        },
    },
    "loggers": {
        # Info loggers
        "aiogram": {"level": "INFO", "handlers": ["info_handler"]},
        "apscheduler.scheduler": {"level": "INFO", "handlers": ["info_handler"]},
        # Error loggers
        "my_logger": {"level": "ERROR", "handlers": ["error_handler"]},
        "apscheduler": {"level": "ERROR", "handlers": ["error_handler"]},
    },
}
