from flask import Blueprint
from flask_restplus import Api

from .auth_ns import auth_ns as Authentication_Namespace
from .ride_ns import ride_ns as Rides_Namespace

api_bp = Blueprint("api_Bp", __name__, url_prefix="/api/v1")




api = Api(api_bp, title="RMI-API",version="1.0",
            description="Carpooling API to share rides",
            doc='/doc/'
        )

api.add_namespace(Authentication_Namespace)
api.add_namespace(Rides_Namespace)
