from flask import Blueprint
from flask_restful import Api

from .views import RidesResource, RideResource, \
    RideRequest, RideRequests, RequestAction, \
    RideCreation, RideUpdate

ride_BP =  Blueprint('ride', __name__, url_prefix='/api/v1')

ride_api = Api(ride_BP)
ride_api.add_resource(RidesResource, '/rides', endpoint="rides") # get all rides
ride_api.add_resource(RideCreation,'/users/rides', endpoint="create") # create a ride

ride_api.add_resource(RideResource, '/rides/<rideId>', endpoint="view") # view a ride

ride_api.add_resource(RideUpdate, '/users/rides/<rideId>', endpoint="update") # update ride

ride_api.add_resource(RideRequest, '/rides/<rideId>/requests', 
                        endpoint="request") # make/retract request to join ride

ride_api.add_resource(RideRequests, '/users/rides/<rideId>/requests', 
                        endpoint="requests") #fetch all ride requests

ride_api.add_resource(RequestAction, 
                        '/users/rides/<rideId>/requests/<requestId>',
                        endpoint="request_action") # accept or reject request

