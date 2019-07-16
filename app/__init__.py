from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import app_configs

def create_app(env_config="config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configs[env_config])
    app.url_map.strict_slashes = False

    JWTManager(app)

    from .db import init_app
    init_app(app)

    from .auth_bp import auth_BP as Authentication_Blueprint
    app.register_blueprint(Authentication_Blueprint)

    from .ride_bp import ride_BP as Ride_Blueprint
    app.register_blueprint(Ride_Blueprint)

    @app.route("/")
    def home():
        return render_template('home.html')

    return app