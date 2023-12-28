# -*- coding: utf-8 -*-

"""
Configuration test module for Cursus Application
"""

import pytest
import os

from flask import Flask
from dotenv import load_dotenv, find_dotenv

from cursus import create_app
from cursus.util.extensions import assets


@pytest.fixture(scope="session")
def app():
    env_file = find_dotenv(os.path.join("..", ".env"))
    load_dotenv(env_file)

    os.environ["FLASK_ENV"] = "development"
    assets._named_bundles = {}  # pylint: disable=protected-access
    app = create_app("cursus.config.TestingConfig")

    assert os.environ.get("TEST_DATABASE_URL")
    assert app.config["DATABASE_URL"] == os.environ.get("TEST_DATABASE_URL")

    with app.app_context():
        yield app


@pytest.fixture(autouse=True)
def _setup_app_context_for_test(request, app):
    """
    Given app is session-wide, sets up a app context per test to ensure that
    app and request stack is not shared between tests.
    """
    ctx = app.app_context()
    ctx.push()
    yield  # tests will run here
    ctx.pop()


@pytest.fixture(scope="session")
def client(app: Flask):
    ctx = app.test_request_context()
    ctx.push()

    return app.test_client()


@pytest.fixture(scope="session")
def runner(app: Flask):
    yield app.test_cli_runner()


@pytest.fixture()
def db(app, request):
    """Return a newly initialized database"""
    from cursus.util.extensions import db as _db

    with app.app_context():
        yield _db


@pytest.fixture
def admin(app):
    """Return an admin user instance."""
    from cursus.models.user import User, Account

    with app.app_context():
        # Select User based on Account
        user_for_login = (
            User.query.select_from(User)
            .join(
                Account,
                User.id == Account.userId,
            )
            .filter(
                Account.provider == "self",
                User.id == "test",
                Account.id == "test-acc",
            )
            .first()
        )

        yield user_for_login


@pytest.hookimpl
def pytest_configure(config):
    config.addinivalue_line("markers", "config: mark test as config test")
    config.addinivalue_line("markers", "swjs: mark test as swjs test")
    config.addinivalue_line("markers", "robots: mark test as robots test")
    config.addinivalue_line("markers", "images: mark test as images test")
    config.addinivalue_line(
        "markers", "after_request: mark test as after_request test"
    )
