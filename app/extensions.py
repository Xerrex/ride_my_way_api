from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def ext_init_app(app):
    """Intializes extensions with the flask app

    Args:
        app (Flask): an instance of the flask app
    """
    db.init_app(app) # Flask-SqlAlchemy
    migrate.init_app(app, db) # Flask-Migrate
    

