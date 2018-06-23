import os

class Config(object):
    """Parent configuration class for enviroments.
    """
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'I just heard the beat and wrote a few lines'


class Testing(Config):
    """Testing Environment configurations.
    """

    TESTING = True



app_configs = {
    'config':Config,
    'test': Testing
}
