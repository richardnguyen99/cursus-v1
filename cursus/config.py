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
    SWAGGER_API_SPEC_URL = os.environ.get("SWAGGER_API_SPEC_URL")

    # Config for Flask SQLAlchemy and Alembic
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    # Config for Flask Session
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REMEMBER_COOKIE_NAME = "cursus_remember"
    REMEMBER_COOKIE_DURATION = 2592000

    # Config for Flask-Caching
    CACHE_TYPE = os.environ.get("CACHE_TYPE")
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST")
    CACHE_REDIS_PORT = os.environ.get("CACHE_REDIS_PORT")
    CACHE_REDIS_DB = os.environ.get("CACHE_REDIS_DB")
    CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = os.environ.get("CACHE_DEFAULT_TIMEOUT")

    # Config for Flask Assets
    # https://webassets.readthedocs.io/en/latest/builtin_filters.html#uglifyjs
    UGLIFYJS_EXTRA_ARGS = [
        "--compress",
        "--mangle",
        "--toplevel",
        "--wrap",
        "Cursus",
        "--webkit",
        "--module",
    ]

    # https://webassets.readthedocs.io/en/latest/builtin_filters.html#autoprefixer
    AUTOPREFIXER_BROWSER = ["> 1%", "last 2 versions", "ie >= 10", "iOS >= 7"]

    # https://webassets.readthedocs.io/en/latest/builtin_filters.html#javascript-cross-compilers
    # BABEL_PRESETS = "babel-preset-env"
    BABEL_PRESET_ENV_PATH = os.environ.get("BABEL_PRESET_ENV_PATH")

    # Config for OAuth2
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
            "access_type": "offline",
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
    PREFERRED_URL_SCHEME = "https"
