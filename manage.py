# -*- coding: utf-8 -*-
"""Flask Management Script"""

import click
import waitress
import os

from flask.cli import FlaskGroup
from dotenv import load_dotenv

from cursus import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Flask application."""


@cli.command("waitress")
@click.option("--host", default="0.0.0.0", help="Host IP to bind to")
@click.option("--port", default=8000, help="Port to bind to")
def run_waitress(host, port):
    """Run the application using Waitress as the production server."""

    # Load the environment variables from the .env file manually as `waitress`
    # does not include the environment variables loading by default like Flask.
    load_dotenv()

    # Assert some environment variables are set
    assert os.environ.get("DATABASE_URL")
    assert os.environ.get("FLASK_ENV")

    app = create_app()
    print(f"Running waitress on {host}:{port}")

    waitress.serve(app, host=host, port=port)


if __name__ == "__main__":
    cli()
