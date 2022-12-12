import logging

from . import db
from . import class_User
from . import class_SelectedInfo
from . import languages


logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)
