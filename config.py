import os
from pathlib import Path
from datetime import timedelta

basedir = Path(__file__).resolve().parent
database = Path(basedir).joinpath(os.environ.get('DATABASE'))
database_test = Path(basedir).joinpath(os.environ.get('DATABASE_TEST'))


class Config(object):
    """Parent configuration class for enviroments.
    """
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I just heard the beat and wrote a few lines'
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

    # TODO Move to Docker Postgres
    SQLALCHEMY_DATABASE_URI = f'sqlite:////{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    pass

class Testing(Config):
    """Testing Environment configurations.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:////{database_test}'


app_configs = {
    'dev':Development,
    'test': Testing
}
