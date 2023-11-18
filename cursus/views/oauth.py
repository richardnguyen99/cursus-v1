# -*- coding: utf-8 -*-

"""Cursus OAuth module with OAuth2 support
"""

import cuid2
import flask
import secrets
import flask_login
import requests

from urllib.parse import urlencode

from cursus.models import Account, User
from cursus.util.extensions import db
from cursus.util.profile import get_profile
from cursus.util.account import get_account


def authorize(provider: str):
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    provider_data = flask.current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if not provider_data:
        return flask.abort(404)

    flask.session["oauth2_state"] = secrets.token_urlsafe(16)
    next = flask.request.args.get("next")

    query_string = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": flask.url_for(
                "oauth.callback",
                provider=provider,
                next=next,
                _external=True,
            ),
            "scope": " ".join(provider_data["scope"]),
            "response_type": "code",
            "state": flask.session["oauth2_state"],
            "access_type": provider_data.get("access_type", "online"),
        }
    )

    return flask.redirect(f"{provider_data['authorize_url']}?{query_string}")


def callback(provider: str):
    if not flask_login.current_user.is_anonymous:
        return flask.redirect(flask.url_for("views.show", page_name="index"))

    provider_data = flask.current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if not provider_data:
        return flask.abort(404)

    if flask.request.args.get("state") != flask.session["oauth2_state"]:
        return flask.abort(401)

    if "code" not in flask.request.args:
        return flask.abort(401)

    next = flask.request.args.get("next")

    response = requests.post(
        provider_data["token_url"],
        data={
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"],
            "code": flask.request.args.get("code"),
            "redirect_uri": flask.url_for(
                "oauth.callback",
                provider=provider,
                next=next,
                _external=True,
            ),
            "grant_type": "authorization_code",
        },
        headers={"Accept": "application/json"},
    )

    if response.status_code != 200:
        return flask.abort(403)

    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
        return flask.abort(401)

    token_response = response.json()

    response = requests.get(
        provider_data["userinfo"]["url"],
        headers={
            "Authorization": f"Bearer {oauth2_token}",
            "Accept": "application/json",
        },
    )

    if response.status_code != 200:
        return flask.abort(401)

    data_response = response.json()

    uniform_account = get_account(provider, token_response, data_response)
    account_from_database = (
        db.session.query(Account)
        .filter_by(
            provider=uniform_account.provider,
            providerAccountId=uniform_account.providerAccountId,
        )
        .first()
    )

    profile = get_profile(provider, data_response)

    # Account has not registered with this app
    if account_from_database is None:
        profile.id = cuid2.Cuid(length=11).generate()
        uniform_account.userId = profile.id

        db.session.add(profile)
        db.session.add(uniform_account)

    else:
        user = (
            db.session.query(User)
            .filter_by(id=account_from_database.userId)
            .first()
        )

        if user and profile.name != user.name:
            user.name = profile.name

        if user and profile.image != user.image:
            user.image = profile.image

        account_from_database.refresh_token = uniform_account.refresh_token

    db.session.commit()

    print(uniform_account.providerAccountId)

    # Select User based on Account
    user_for_login = (
        db.session.query(User)
        .join(
            Account,
            User.id == Account.userId,
        )
        .filter(
            Account.provider == uniform_account.provider,
            Account.providerAccountId == uniform_account.providerAccountId,
        )
        .first()
    )

    flask_login.login_user(user_for_login, remember=True)

    if next is not None:
        return flask.redirect(flask.url_for(next))

    return flask.redirect(flask.url_for("views.show", page_name="index"))
