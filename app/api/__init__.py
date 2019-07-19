from flask import Blueprint
from flask_restplus import Api

from app.api.auth_ns import api as Authentication_Services
from app.api.ride_ns import api as Ride_operations

api_bp = Blueprint("api_bp", __name__, url_prefix="/api/v1")


authorizations = {
    "bearer": { 
        'type': 'apiKey', 
        'in':'header', 
        'name': 'Authorization',
        'template': 'Bearer {apiKey}'
    }
}

api_v1 = Api(api_bp, title="RMW",
            version='V1.0',
            description='Ride my way Carpooling API',
            authorizations=authorizations
)

api_v1.add_namespace(Authentication_Services, path='/auth')
api_v1.add_namespace(Ride_operations, path="/")
