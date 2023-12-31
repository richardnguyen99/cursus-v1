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


def test_apis_valid_preflight_requests(app, client, admin):
    with app.test_request_context():
        login_user(admin)

        user = app.login_manager._user_callback(admin.id)

        option_res = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "X-CURSUS-API-TOKEN": user.active_token,
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "x-cursus-api-token",
            },
        )

        assert option_res.status_code == 200

        logout_user()


def test_apis_missing_origin_preflight_requests(app, client, admin):
    with app.test_request_context():
        login_user(admin)

        user = app.login_manager._user_callback(admin.id)

        option_res = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "X-CURSUS-API-TOKEN": user.active_token,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "x-cursus-api-token",
            },
        )

        assert option_res.status_code == 400
        assert option_res.headers["Content-Type"] == "application/json"

        data = option_res.get_json()

        assert data["error"]
        assert data["error"]["code"] == 400
        assert data["error"]["message"] == "Bad Request"
        assert data["error"]["reason"] == "Invalid preflight request"

        logout_user()


def test_apis_request_method_preflight_requests(app, client, admin):
    with app.test_request_context():
        login_user(admin)

        user = app.login_manager._user_callback(admin.id)

        invalid_option_res1 = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "Origin": "http://localhost",
                "X-CURSUS-API-TOKEN": user.active_token,
                "Access-Control-Request-Headers": "x-cursus-api-token",
            },
        )

        assert invalid_option_res1.status_code == 400
        assert (
            invalid_option_res1.headers["Content-Type"] == "application/json"
        )

        data = invalid_option_res1.get_json()

        assert data["error"]
        assert data["error"]["code"] == 400
        assert data["error"]["message"] == "Bad Request"
        assert data["error"]["reason"] == "Invalid preflight request"

        invalid_option_res2 = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "Origin": "http://localhost",
                "X-CURSUS-API-TOKEN": user.active_token,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "x-cursus-api-token",
            },
        )

        assert invalid_option_res2.status_code == 400
        assert (
            invalid_option_res2.headers["Content-Type"] == "application/json"
        )

        data = invalid_option_res2.get_json()

        assert data["error"]
        assert data["error"]["code"] == 400
        assert data["error"]["message"] == "Bad Request"
        assert data["error"]["reason"] == "Invalid preflight request"

        logout_user()


def test_apis_request_headers_preflight_request(app, client, admin):
    with app.test_request_context():
        login_user(admin)

        user = app.login_manager._user_callback(admin.id)

        invalid_option_res1 = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "Origin": "http://localhost",
                "X-CURSUS-API-TOKEN": user.active_token,
                "Access-Control-Request-Method": "GET",
            },
        )

        assert invalid_option_res1.status_code == 400
        assert (
            invalid_option_res1.headers["Content-Type"] == "application/json"
        )

        data = invalid_option_res1.get_json()

        assert data["error"]
        assert data["error"]["code"] == 400
        assert data["error"]["message"] == "Bad Request"
        assert data["error"]["reason"] == "Invalid preflight request"

        invalid_option_res2 = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "Origin": "http://localhost",
                "X-CURSUS-API-TOKEN": user.active_token,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "x-curs-api-token",
            },
        )

        assert invalid_option_res2.status_code == 400
        assert (
            invalid_option_res2.headers["Content-Type"] == "application/json"
        )

        data = invalid_option_res2.get_json()

        assert data["error"]
        assert data["error"]["code"] == 400
        assert data["error"]["message"] == "Bad Request"
        assert data["error"]["reason"] == "Invalid preflight request"

        valid_option_res = client.options(
            "/api/v1/search/university?query=harvard",
            headers={
                "Origin": "http://localhost",
                "X-CURSUS-API-TOKEN": user.active_token,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "X-CURSUS-API-TOKEN",
            },
        )

        assert valid_option_res.status_code == 200

        logout_user()


def test_apis_with_invalid_method_requests(app, client, admin):
    app_context = app.test_request_context()

    app_context.push()

    login_user(admin)

    user = app.login_manager._user_callback(admin.id)

    get_res = client.get(
        "/api/v1/search/university?query=harvard",
        headers={
            "X-CURSUS-API-TOKEN": user.active_token,
        },
    )

    options_res = client.options(
        "/api/v1/search/university?query=harvard",
        headers={
            "X-CURSUS-API-TOKEN": user.active_token,
            "Origin": "*",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-CURSUS-API-TOKEN",
        },
    )

    post_res = client.post(
        "/api/v1/search/university?query=harvard",
        headers={
            "X-CURSUS-API-TOKEN": user.active_token,
        },
    )

    put_res = client.put(
        "/api/v1/search/university?query=harvard",
        headers={
            "X-CURSUS-API-TOKEN": user.active_token,
        },
    )

    delete_res = client.delete(
        "/api/v1/search/university?query=harvard",
        headers={"X-CURSUS-API-TOKEN": user.active_token},
    )

    assert get_res.status_code == 200
    assert options_res.status_code == 200

    assert post_res.status_code == 405
    assert put_res.status_code == 405
    assert delete_res.status_code == 405

    assert post_res.data
    assert put_res.data
    assert delete_res.data

    post_json = post_res.get_json()
    put_json = put_res.get_json()
    delete_json = delete_res.get_json()

    assert post_json["error"]
    assert put_json["error"]
    assert delete_json["error"]

    assert post_json["error"]["code"] == 405
    assert put_json["error"]["code"] == 405
    assert delete_json["error"]["code"] == 405

    assert post_json["error"]["message"] == "Method Not Allowed"
    assert put_json["error"]["message"] == "Method Not Allowed"
    assert delete_json["error"]["message"] == "Method Not Allowed"

    logout_user()

    app_context.pop()


def test_apis_with_not_found_handler(app, client, admin):
    app_context = app.test_request_context()

    app_context.push()

    login_user(admin)

    user = app.login_manager._user_callback(admin.id)

    not_found_search = client.get(
        "/api/v1/unknown/",
        headers={
            "X-CURSUS-API-TOKEN": user.active_token,
        },
    )

    assert not_found_search.status_code == 404
    assert not_found_search.headers["Content-Type"] == "application/json"

    data = not_found_search.get_json()

    assert data["error"]
    assert data["error"]["code"] == 404
    assert data["error"]["message"] == "Not Found"
    assert (
        data["error"]["reason"]
        == "API endpoint, `/api/v1/unknown/`, not found"
    )

    logout_user()

    app_context.pop()
