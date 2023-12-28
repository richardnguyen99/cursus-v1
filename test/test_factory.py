import os
import flask

import pytest
import json

from webassets.bundle import Bundle
from dotenv import load_dotenv, find_dotenv
from flask_login import current_user, login_user

from cursus import create_app
from cursus.util.extensions import assets


@pytest.mark.config
def test_config():
    env_file = find_dotenv(".env")
    load_dotenv(env_file, override=True)

    assets._named_bundles = {}  # pylint: disable=protected-access
    os.environ["APP_SETTINGS"] = "cursus.config.DevConfig"
    app = create_app()

    assert not app.config["TESTING"]
    assert app.config["FLASK_ENV"] == "development"
    assert app.config["DATABASE_URL"] == os.environ.get("DATABASE_URL")

    assets._named_bundles = {}  # pylint: disable=protected-access
    app = create_app("cursus.config.TestingConfig")

    assert app.config["TESTING"]
    assert app.config["FLASK_ENV"] == "testing"
    assert app.config["DATABASE_URL"] == os.environ.get("TEST_DATABASE_URL")


@pytest.mark.swjs
def test_swjs(client):
    response = client.get("/sw.js")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/javascript"
    assert response.headers["Cache-Control"] == "no-cache"


@pytest.mark.robots
def test_robots(client):
    response = client.get("/robots.txt")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain"
    assert response.headers["Cache-Control"] == "no-cache"


@pytest.mark.images
def test_images(client):
    response = client.get("/static/img/logo-16.png")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["Cache-Control"] == "public, max-age=31536000"


@pytest.mark.after_request
def test_after_request(client):
    response = client.get("/static/img/logo-16.png")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["Cache-Control"] == "public, max-age=31536000"

    response_without_cache = client.get(
        "/static/img/logo-16.png", headers={"Cache-Control": "no-cache"}
    )

    assert response_without_cache.status_code == 200
    assert response_without_cache.headers["Content-Type"] == "image/png"
    assert response_without_cache.headers["Cache-Control"] == "no-cache"

    ###########################################################################
    #                                                                         #
    #                       Common headers for both scenarios                 #
    #                                                                         #
    ###########################################################################

    assert response.headers["ETag"]
    assert response_without_cache.headers["ETag"]
    assert response.headers["ETag"] == response_without_cache.headers["ETag"]

    assert response.headers["Last-Modified"]
    assert response_without_cache.headers["Last-Modified"]
    assert (
        response.headers["Last-Modified"]
        == response_without_cache.headers["Last-Modified"]
    )

    assert response.headers["Access-Control-Allow-Methods"]
    assert response_without_cache.headers["Access-Control-Allow-Methods"]
    assert (
        response.headers["Access-Control-Allow-Methods"]
        == response_without_cache.headers["Access-Control-Allow-Methods"]
    )

    assert response.headers["Access-Control-Allow-Origin"]
    assert response_without_cache.headers["Access-Control-Allow-Origin"]
    assert (
        response.headers["Access-Control-Allow-Origin"]
        == response_without_cache.headers["Access-Control-Allow-Origin"]
    )

    assert response.headers["Access-Control-Max-Age"] == "3600"
    assert response_without_cache.headers["Access-Control-Max-Age"] == "3600"
    assert (
        response.headers["Access-Control-Max-Age"]
        == response_without_cache.headers["Access-Control-Max-Age"]
    )


def test_context_processor(client):
    from cursus.util.generate_content_hash import generate_content_hash

    # Here, [None] means the top-level Flask application, i.e. in the
    # `create_app` function, `app = Flask(__name__)`.
    # The 2 means the index of the `inject_content_hash` function in the list
    f = client.application.template_context_processors[None][2]

    # print(client.application.template_context_processors) -> list of BPs
    # print(client.application.template_context_processors[None]) -> functions

    image_path = os.path.join(
        flask.current_app.root_path,
        "static",
        "img",
        "logo-16.png",
    )

    hashed = generate_content_hash(image_path)

    assert f is not None
    assert f()["content_hash_for_image"]("logo-16.png") == hashed


def test_unauthorized_handler(client):
    response = client.get("/profile")

    assert response.status_code == 302

    # Assert flash message from response
    with client.session_transaction() as session:
        # Flask flashes are stored in the session as a list of tuples
        # (message, category)

        assert len(session["_flashes"]) == 1

        # print(session["_flashes"])

        assert (
            session["_flashes"][0][1]
            == "You have to be logged in to access this page."
        )


def test_logout(client):
    response = client.get("/logout")

    assert response.status_code == 302


def test_extensions(client):
    assert client.application.extensions["sqlalchemy"]
    assert client.application.extensions["migrate"]
    assert client.application.extensions["flask-marshmallow"]
    assert client.application.extensions["cache"]
    assert client.application.login_manager


def test_load_user_id(app, client, db, admin):
    with app.test_request_context():
        login_user(admin)
        assert current_user.id == admin.id
        loaded_user = app.login_manager._user_callback(current_user.id)

        assert loaded_user.id == admin.id
        assert loaded_user.email == admin.email
        assert loaded_user.name == admin.name
        assert loaded_user.provider == admin.provider
        assert loaded_user.active_token == admin.active_token

        none_user = app.login_manager._user_callback("nah")

        assert none_user is None

        res = client.get("/logout")

        assert res.status_code == 302
        assert current_user.is_anonymous
        assert res.headers["Location"] == "/"


def test_hello(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == json.dumps({"message": "pong"}).encode()
