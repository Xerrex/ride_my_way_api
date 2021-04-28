import os
from pathlib import Path
from datetime import timedelta

basedir = Path(__file__).resolve().parent

class Config(object):
    """Parent configuration class for enviroments.
    """
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I just heard the beat and wrote a few lines'
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

    DATABASE = Path(basedir).joinpath(os.environ.get('DATABASE'))
    # DATABASE_HOST = os.environ.get('DATABASE_HOST')
    # DATABASE_USER = os.environ.get('DATABASE_USER')
    # DATABASE_PASS = os.environ.get('DATABASE_PASS')

class Development(Config):
    pass

class Testing(Config):
    """Testing Environment configurations.
    """

    TESTING = True
    DATABASE = os.environ.get('DATABASE_TEST')


app_configs = {
    'dev':Development,
    'test': Testing
}
