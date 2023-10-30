# -*- coding: utf-8 -*-

"""List of extensions used by this application
"""

from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class Base(DeclarativeBase):
    """Base class for all models"""


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
