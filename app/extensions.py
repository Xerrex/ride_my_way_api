from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .db import init_app as sqlite3_init_app

db = SQLAlchemy()
migrate = Migrate()

def ext_init_app(app):
    """Intializes extensions with the flask app

    Args:
        app (Flask): an instance of the flask app
    """
    sqlite3_init_app(app) # TODO replace with ORM
    db.init_app(app) # Flask-SqlAlchemy
    migrate.init_app(app, db) # Flask-Migrate
    

