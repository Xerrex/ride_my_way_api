import sqlite3
from uuid import uuid4
from datetime import datetime, timedelta


import click
from flask import current_app, g
from flask.cli import with_appcontext

def  get_db():
    """Gets the db for request.

    returns a Database connection
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory = sqlite3.Row
        return g.db


def close_db(e=None):
    """If this request connected to the 
        database, close the connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def initialize():
    """Clear existing data and create new tables.

    Should be run the first time only
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))   


@click.group()
def db():
    """db operation commands"""
    pass


@db.command()
@with_appcontext
def init():
    """Clear existing data & create 
        initial db tables.
    """

    initialize()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask 
    app. This is called by the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(db)
