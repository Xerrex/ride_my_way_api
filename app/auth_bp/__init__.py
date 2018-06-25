from flask import Blueprint
from flask_restful import Api

from .views import RegisterResource, LoginResource, LogoutResource

auth_BP = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

auth_api = Api(auth_BP)

auth_api.add_resource(RegisterResource, '/register', endpoint="register")
auth_api.add_resource(LoginResource, '/login', endpoint="login")
auth_api.add_resource(LogoutResource, '/logout', endpoint="logout")

