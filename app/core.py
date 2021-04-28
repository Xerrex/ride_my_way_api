from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from config import app_configs

def create_app(config="dev"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configs[config])
    app.url_map.strict_slashes = False

    JWTManager(app)

    from .db import init_app
    init_app(app)

    from .api import api_bp as API_Blueprint
    app.register_blueprint(API_Blueprint)


    @app.route("/")
    def home():
        return render_template('home.html')

    return app