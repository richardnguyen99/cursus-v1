# -*- coding: utf-8 -*-

"""
Configuration test module for Cursus Application
"""

import os
import tempfile
import pytest

from flask import Flask
from dotenv import load_dotenv, find_dotenv

from cursus import create_app
from cursus.util.extensions import assets


@pytest.fixture(scope="session", autouse=True)
def app():
    env_file = find_dotenv(".env")
    load_dotenv(env_file, override=True)
    db_fd, db_path = tempfile.mkstemp()

    assets._named_bundles = {}  # pylint: disable=protected-access
    app = create_app("cursus.config.TestingConfig")

    with app.app_context():
        print(app.config["TESTING"])

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(autouse=True)
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()
