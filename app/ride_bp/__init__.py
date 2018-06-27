from flask import Blueprint
from flask_restful import Api

from .views import RidesResource, RideResource, \
    RideRequestsResource, RequestActionResource

ride_BP =  Blueprint('ride', __name__, url_prefix='/api/v1')

ride_api = Api(ride_BP)
ride_api.add_resource(RidesResource, '/rides', endpoint="rides")
ride_api.add_resource(RideResource, '/rides/<rideId>', endpoint="ride")

ride_api.add_resource(RideRequestsResource, '/rides/<rideId>/requests', 
                        endpoint="request")

ride_api.add_resource(RequestActionResource, 
                        '/rides/<rideId>/requests/<requestId>',
                        endpoint="request_action")

