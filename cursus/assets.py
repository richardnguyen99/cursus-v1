# -*- coding: utf-8 -*-

"""Cursus Assets and bundles module

This submodule contains Flask-Assets configurations and static bundles used by
the web application
"""

import flask

from flask_assets import Bundle
from webassets.bundle import get_filter

scss_bundle = Bundle(
    "scss/global.scss",
    filters="scss,autoprefixer6,cssmin",
    output="css/min.bundle.css",
    # https://webassets.readthedocs.io/en/latest/bundles.html#bundles
    depends="scss/**/_*.scss",
)

babel_filter = get_filter(
    "babel",
    presets=flask.current_app.config["BABEL_PRESET_ENV_PATH"],
)

js_bundle = Bundle(
    Bundle(
        "js/app.js",
        "js/dropdown.js",
        "js/index.js",
        "js/profile.js",
        output="js/min.bundle.js",
        filters=(babel_filter, "uglifyjs"),
    ),
    Bundle(
        "js/vendor/prism.js",
        output="js/vendor.bundle.js",
    ),
    depends="js/**/*",
)
