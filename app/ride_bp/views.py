"""Defines ride Resources"""
from flask import session
from flask_restful import Resource, reqparse

from app.validators import string_validator, date_validator

from app.data.ride_data import create_ride, get_rides,\
    rides_generator, get_ride, abort_ride_not_found, \
    make_request, abort_ride_request_found,retract_request, \
    update_ride, get_ride_requests


def check_active_session():
    """Check if there is an active user sssion
    """
    if 'userID' not in session:
        return {
            "message":"You must be logged in to Create new ride",
            "login_link": "/api/v1/auth/login"
        }, 401


class RidesResource(Resource):
    """Handles Rides Resource
    
    endpoint /rides
    """

    ride_parser = reqparse.RequestParser()
    ride_parser.add_argument('starting_point', type=string_validator,
                                required=True, location='json')
    
    ride_parser.add_argument('destination', type=string_validator,
                                required=True, location='json')

    ride_parser.add_argument('depart_time', type=date_validator,
                                required=True, location='json')

    ride_parser.add_argument('eta', type=date_validator,
                                required=True, location='json')
    
    ride_parser.add_argument('seats', type=int,
                                required=True, location='json')
    
    ride_parser.add_argument('vehicle', type=string_validator,
                                required=True, location='json')


    def post(self):
        """Creates a new ride
        """

        check_active_session()

        ride_args = self.ride_parser.parse_args()

        ride = create_ride(starting_point=ride_args['starting_point'],
                    destination=ride_args['destination'],
                    depart_time=ride_args['depart_time'],
                    eta=ride_args['eta'],
                    vehicle=ride_args['vehicle'],
                    seats=ride_args['seats'],
                    driver=session['userID'])
        
        return {
            "message":"New ride offer was created",
            "view_ride":"/api/v1/rides/{}".format(ride[0])
        }, 201


    def get(self):
        """Get all available rides
        """
        check_active_session()

        rides_generator(20)
        return get_rides(), 200


class RideResource(Resource):
    """Handles the ride resources
    
    endpoint: /api/v1/rides/<rideId>
    """

    def get(self,rideId):
        """Gets a rides whose id is specicified
        
        Arguments:
            rideId {String} -- Unique Ride identifier.
        """
        check_active_session()

        if not abort_ride_not_found(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        return get_ride(rideId), 200

    
    update_parser = reqparse.RequestParser()
    update_parser.add_argument('starting_point', type=string_validator,
                                required=True, location='json')
    
    update_parser.add_argument('destination', type=string_validator,
                                required=True, location='json')

    update_parser.add_argument('depart_time', type=date_validator,
                                required=True, location='json')

    update_parser.add_argument('eta', type=date_validator,
                                required=True, location='json')
    
    update_parser.add_argument('seats', type=int,
                                required=True, location='json')
    
    update_parser.add_argument('vehicle', type=string_validator,
                                required=True, location='json')

    def put(self, rideId):
        """update Ride details
        
        Arguments:
            rideId {String} -- Unique Ride identifier.
        """
        check_active_session()

        if not abort_ride_not_found(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        ride = get_ride(rideId)

        if ride['driver']==session['userID']:
            update_args = self.update_parser.parse_args()
            update_ride(rideId, 
                        starting_point=update_args['starting_point'],
                        destination=update_args['destination'],
                        depart_time=update_args['depart_time'],
                        eta=update_args['eta'],
                        vehicle=update_args['vehicle'],
                        seats=update_args['seats'])
            return {
                "message":"Ride details were update"
            },200
            
        return {
            "message":"Your do not own the ride"
        }, 401
        

class RideRequestResource(Resource):
    """Handles the Ride Requests resources

    endpoint: /api/v1/rides/<rideId>/requests
    """
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('destination', type=string_validator,
                            required=True, location='json')

    def post(self, rideId):
        """Makes a request to join a ride
        
        Arguments:
            rideId {String} -- Unique Identifier of a ride
        """
        check_active_session()

        req_args = self.req_parser.parse_args()

        if not abort_ride_not_found(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        abort_ride_request_found(rideId, session['userID'])

        req = make_request(session['userID'], req_args['destination'], rideId)

        return{
            "message": "You have requested to join the ride",
            "view_request": '/api/v1/rides/{}/requests/{}'.format(rideId,req[0])
        }, 201

    def delete(self, rideId):
        """Retracts a Request to join a ride
        
        Arguments:
            rideId {String} -- Unique Indentifier of a ride
        """
        check_active_session()

        if not abort_ride_not_found(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        response = retract_request(session['userID'], rideId)

        return{
            "message": response
        }, 204

    def get(self, rideId):
        """Fetch all requests on a ride
        
        Arguments:
            rideId {String} -- Unique Ride Identifier
        """
        check_active_session()

        if not abort_ride_not_found(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        ride = get_ride(rideId)
        if ride['driver'] == session['userID']:
            # get ride requests
            return get_ride_requests(rideId), 200
        return {
            "message": "Your not authorized to view these requests"
        }, 401
