from psycopg2 import connect


import click
from flask import current_app, g
from flask.cli import with_appcontext

def  get_db():
    """Gets the db for request.

    returns a Database connect
    """
    if 'db' not in g:
        g.db = connect(
                host=current_app.config['DATABASE_HOST'],
                dbname=current_app.config['DATABASE'], 
                user=current_app.config['DATABASE_USER'], 
                password=current_app.config['DATABASE_PASS']
            )
        return g.db


def commit_db():
    """Make database changes persistent"""
    get_db().commit()


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def initialize():
    """Clear existing data and create new tables.

    Should be run the first time only
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f, db.cursor() as cursor:
        cursor.execute(f.read().decode('utf8'))
        

@click.group()
def db():
    """db operation commands"""
    pass


@db.command()
@with_appcontext
def init():
    """Create initial db tables"""

    initialize()
    click.echo('Initialized the database.')


@db.command()
@with_appcontext
def commit():
    """Make db changes persistent"""
    commit_db()
    click.echo('Database changes made persistent')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(db)
