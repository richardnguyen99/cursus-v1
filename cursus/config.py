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
    OAUTH2_PROVIDERS = {
        # Google OAuth 2.0 documentation:
        # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
        "google": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "scope": [
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
            ],
            "userinfo": {
                "url": "https://www.googleapis.com/oauth2/v3/userinfo",
            },
        },
        "github": {
            "client_id": os.environ.get("GITHUB_CLIENT_ID"),
            "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
            "authorize_url": "https://github.com/login/oauth/authorize",
            "token_url": "https://github.com/login/oauth/access_token",
            "scope": ["read:user", "user:email"],
            "userinfo": {
                "url": "https://api.github.com/user",
            },
        },
        "discord": {
            "client_id": os.environ.get("DISCORD_CLIENT_ID"),
            "client_secret": os.environ.get("DISCORD_CLIENT_SECRET"),
            "authorize_url": "https://discord.com/api/oauth2/authorize",
            "token_url": "https://discord.com/api/oauth2/token",
            "scope": ["identify", "email"],
            "userinfo": {
                "url": "https://discord.com/api/users/@me",
            },
        },
    }


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
