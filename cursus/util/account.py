# -*- coding: utf-8 -*-

"""
Account functions to obtain account information from OAuth2 providers.
"""

from typing import Dict

from cursus.models import Account

__all__ = [
    "get_account",
]


def get_account(
    provider: str,
    token: Dict[str, str],
    data: Dict[str, str],
) -> Account:
    """Returns the Account-compatible profile from the given provider and data.

    :param token: Raw json-encoded token response from OAuth2 Provider.
    :param data: Raw json-encoded data response from OAuth2 Provider.
    """

    if provider == "google":
        return _get_google_account(token, data)

    if provider == "github":
        return _get_github_account(token, data)

    if provider == "discord":
        return _get_discord_account(token, data)

    raise ValueError(f"Unknown provider: {provider}")


def _get_google_account(
    token: Dict[str, str],
    data: Dict[str, str],
) -> Account:
    """Returns the Account-compatible profile from the data given by Google.

    :param token: Raw json-encoded token response from Google OAuth2.
    :param data: Raw json-encoded data response from Google OAuth2.
    """

    account = Account(
        auth_type="oauth2",
        provider="google",
        providerAccountId=data["sub"],
        refresh_token=token.get("refresh_token", None),
    )

    return account


def _get_github_account(
    token: Dict[str, str],
    data: Dict[str, str],
) -> Account:
    """Returns the Account-compatible profile from the data given by GitHub.

    :param token: Raw json-encoded token response from Google OAuth2.
    :param data: Raw json-encoded data response from Google OAuth2.
    """

    account = Account(
        auth_type="oauth2",
        provider="github",
        providerAccountId=str(data["id"]),
        refresh_token=token.get("refresh_token", None),
    )

    return account


def _get_discord_account(
    token: Dict[str, str],
    data: Dict[str, str],
) -> Account:
    """Returns the Account-compatible profile from the data given by Discord.

    :param token: Raw json-encoded token response from Google OAuth2.
    :param data: Raw json-encoded data response from Google OAuth2.
    """

    account = Account(
        auth_type="oauth2",
        provider="discord",
        providerAccountId=data["id"],
        refresh_token=token.get("refresh_token", None),
    )

    return account
