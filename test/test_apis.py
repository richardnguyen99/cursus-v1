# -*- coding: utf-8 -*-

"""
Test module for Cursus API endpoints

Most testings are done with API endpoints to ensure that the API is working
correctly, with or without an API token key. Plus, it will check if the 
headers, the cache and the database are working appropriately.
"""

from flask_login import current_user, login_user, logout_user


def test_apis_without_key(client):
    res = client.get("/api/v1/search?query=harvard")

    assert res.status_code == 401
    assert res.headers["Content-Type"] == "application/json"

    json_data = res.get_json()

    assert json_data["error"]

    error_data = json_data["error"]

    assert error_data["code"]
    assert error_data["message"]
    assert error_data["reason"]

    assert error_data["code"] == 401
    assert error_data["message"] == "Unauthorized"
    assert (
        error_data["reason"] == "API endpoints require an authorized API token"
    )


def test_apis_with_key(app, client, admin):
    with app.test_request_context():
        login_user(admin)

        user = app.login_manager._user_callback(admin.id)

        res = client.get(
            "/api/v1/search/university?query=harvard",
            headers={"X-CURSUS-API-TOKEN": user.active_token},
        )

        print(res.get_json())

        assert res.status_code == 200

        logout_user()
