# -*- coding: utf-8 -*-

"""Cursus OAuth module with OAuth2 support
"""

import flask


def authorize():
    """OAuth login view function"""
    return flask.render_template("login.html")
