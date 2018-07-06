import os
from datetime import timedelta

class Config(object):
    """Parent configuration class for enviroments.
    """
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I just heard the beat and wrote a few lines'
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

    DATABASE = os.environ.get('DATABASE')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASS = os.environ.get('DATABASE_PASS')


class Testing(Config):
    """Testing Environment configurations.
    """

    TESTING = True
    DATABASE = os.environ.get('DATABASE_TEST')


app_configs = {
    'config':Config,
    'test': Testing
}
