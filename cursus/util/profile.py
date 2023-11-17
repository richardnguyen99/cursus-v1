# -*- coding: utf-8 -*-

"""
Profile functions to obtain user information from OAuth2 providers.
"""

from typing import Dict

from cursus.models import User

__all__ = [
    "get_profile",
]


def get_profile(provider: str, data: Dict[str, str]) -> User:
    """Returns the User-compatible profile from the given provider and data.

    :param provider: String representing the provider name.
    :param data: Raw json-encoded data from OAuth2.
    """

    if provider == "google":
        return _get_google_profile(data)

    if provider == "github":
        return _get_github_profile(data)

    if provider == "discord":
        return _get_discord_profile(data)

    raise ValueError(f"Unknown provider: {provider}")


def _get_google_profile(data: Dict[str, str]) -> User:
    """Returns the User-compatible profile from the data given by Google.

    :param data: Raw json-encoded data from Google OAuth2.
    """

    user = User(
        name=data["name"],
        email=data["email"],
        image=data["picture"],
    )

    return user


def _get_github_profile(data: Dict[str, str]) -> User:
    """Returns the User-compatible profile from the data given by GitHub.

    :param data: Raw json-encoded data from GitHub OAuth2.
    """

    return User(
        name=data["name"],
        email=data["email"],
        image=data["avatar_url"],
    )


def _get_discord_profile(data: Dict[str, str]) -> User:
    """Returns the User-compatible profile from the data given by Discord.

    :param data: Raw json-encoded data from Discord OAuth2.
    """

    image = (
        f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"
    )

    return User(
        name=data["global_name"],
        email=data["email"],
        image=image,
    )
