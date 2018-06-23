from flask import Flask

from config import app_configs

def create_app(env_config="config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configs[env_config])

    return app