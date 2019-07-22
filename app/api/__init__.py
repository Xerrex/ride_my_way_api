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

# RegisterResource, '/register', endpoint="register"
# LoginResource, '/login', endpoint="login"
# LogoutResource, '/logout', endpoint="logout"

# RidesResource, '/rides', endpoint="rides" # get all rides
# RideCreation,'/users/rides', endpoint="create"# create a ride

# RideResource, '/rides/<rideId>', endpoint="view"# view a ride

# RideUpdate, '/users/rides/<rideId>', endpoint="update"# update ride

# RideRequest, '/rides/<rideId>/requests', endpoint="request"# make/retract

# RideRequests, '/users/rides/<rideId>/requests', endpoint="requests"# all ride requests

# RequestAction, '/users/rides/<rideId>/requests/<requestId>', endpoint="request_action"# respond request

