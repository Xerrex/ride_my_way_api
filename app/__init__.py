from flask import Flask

from config import app_configs

def create_app(env_config="config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configs[env_config])

    from .db import init_app
    init_app(app)

    from .auth_bp import auth_BP as Authentication_Blueprint
    app.register_blueprint(Authentication_Blueprint)

    from .ride_bp import ride_BP as Ride_Blueprint
    app.register_blueprint(Ride_Blueprint)

    return app