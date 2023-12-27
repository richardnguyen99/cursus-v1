import json

from dotenv import load_dotenv, find_dotenv

from cursus import create_app
from cursus.util.extensions import assets


def test_config():
    env_file = find_dotenv(".env")
    load_dotenv(env_file, override=True)

    assets._named_bundles = {}  # pylint: disable=protected-access
    app = create_app()

    assert not app.config["TESTING"]

    assets._named_bundles = {}  # pylint: disable=protected-access
    app = create_app("cursus.config.TestingConfig")

    assert app.config["TESTING"]


def test_hello(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.data == json.dumps({"message": "pong"}).encode()
