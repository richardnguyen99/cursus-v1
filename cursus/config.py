# -*- coding: utf-8 -*-

"""OS module providing functionalities to work with operating system"""
import os


# from dotenv import load_dotenv

# We don't need to load the .env file here manually


class Config(object):
    """Base configuration class for the application

    This class contains all the default configuration variables that are used
    accross the stages. The environment variables are loaded from the root
    .env file by Flask itself (with `python-dotenv` installed).

    """

    TESTING = False
    DEBUG = False
    DATABASE_URL = os.environ.get("DATABASE_URL")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevConfig(Config):
    """Development configuration class for the application

    This class contains all the development configuration variables that are
    used during development. It inherits from the base configuration class and
    overrides some variables to suit the development environment.

    """

    DEBUG = True
    CSRF_ENABLED = True
    LOG_LEVEL = "DEBUG"


class ProdConfig(Config):
    """Production configuration class for the application

    This class contains all the production configuration variables that are
    used during deployment and production. It inherits from the base
    configuration class and overrides some variables to suit the production
    environment.
    """

    DEBUG = False
    LOG_LEVEL = "INFO"
