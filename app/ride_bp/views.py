"""Defines ride Resources"""
from flask import session
from flask_restful import Resource, reqparse

from app.validators import string_validator, date_validator

from app.data.ride_data import create_ride, get_rides, rides_generator

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

        if 'userID' not in session:
            return {
                "message":"You must be logged in to Create new ride",
                "login_link": "/api/v1/auth/login"
            }, 401

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
        rides_generator(20)
        return get_rides(), 200



        


