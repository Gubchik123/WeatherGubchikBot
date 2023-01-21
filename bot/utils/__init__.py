import logging.config

from . import db
from . import languages
from . import class_User
from . import class_SelectedInfo
from .logging_settings import logger_config


logging.config.dictConfig(logger_config)  # Set up logging config
