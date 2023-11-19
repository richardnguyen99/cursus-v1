# -*- coding: utf-8 -*-

"""List of extensions used by this application
"""

from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_assets import Environment


class Base(DeclarativeBase):
    """Base class for all models"""


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
ma = Marshmallow()
login_manager = LoginManager()
assets = Environment()
