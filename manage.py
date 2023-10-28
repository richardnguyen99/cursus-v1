"""Python Module to support options and commands in a CLI."""
import click

from flask.cli import FlaskGroup

from cursus import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management script for the Flask application."""
