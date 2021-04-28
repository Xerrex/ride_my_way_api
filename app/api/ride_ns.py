"""Defines ride Resources"""
from flask.helpers import url_for
from flask_restplus import Namespace, Resource, \
                            reqparse, abort, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.validators import string_validator, \
                            date_validator, action_validator

from app.data.ride_data import create_ride, get_rides,\
    get_ride, make_request, abort_ride_request_already_made, \
    retract_request, get_ride_requests, \
    abort_request_not_found, get_request, \
    update_request_status, update_ride, \
    abort_active_ride, abort_ride_not_found

ride_ns = Namespace("Ride", description="Ride operations",
                    path="/")


ride = ride_ns.model('Ride',{
    "starting_point": fields.String(description='Where the ride starts'),
    "destination": fields.String(description='Where the ride is going'),
    "depart_time":fields.String(description='Time when the ride starts'),
    "eta":fields.String(description='Time when the ride is expected to arrive'),
    "seats": fields.Integer(description='The Number of available spaces/passengers'),
    "vehicle": fields.String(description='Plates for the vehicle'),
    "driver": fields.String(description='The driver of the ride')
})

# ride_list = ride_ns.model("ride_list", {
#     'id': fields.String(required=True, description='The ID of a ride'),
#     'ride': fields.Nested(ride, description='The Ride')
# })


@ride_ns.route("/users/rides", endpoint="create_ride")
class RideCreation(Resource):
    """Create a ride Resource
    
    Handles /users/rides
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

    @ride_ns.doc("user_create_ride",   
        parser=ride_parser, security="bearer",
        response={
            201: "New ride offer was Created"
        }
    )
    @jwt_required()
    def post(self):
        """Creates a new ride
        """
        
        ride_args = self.ride_parser.parse_args()

        abort_active_ride(ride_args['eta'], get_jwt_identity())
        
        ride_id = create_ride(driver=get_jwt_identity(), **ride_args)
        return {
            "message":"New ride offer was created",
            "view_ride": url_for("api_Bp.view_ride", rideId=ride_id)
        }, 201


@ride_ns.route("/rides", endpoint="view_rides")
class RidesResource(Resource):
    """Handles Rides Resource
    
    endpoint: /rides
    """

    @ride_ns.doc('view_all_rides', security="bearer",
                    responses={200: 'Success, retrieved rides'})
    @jwt_required()
    def get(self):
        """Get all available rides
        """
        rides = get_rides()
        return rides, 200


@ride_ns.route("/rides/<rideId>", endpoint="view_ride")
class RideResource(Resource):
    """Handles the ride resources
    
    endpoint: /rides/<rideId>
    """
    @ride_ns.doc("view_a_ride", 
        params={'rideId': 'Unique Ride identifier'},
        security="bearer",
        response={
            404: "Ride does not exist",
            200: "Ride was Found"
        }
    )
    @jwt_required()
    def get(self,rideId):
        """Gets a rides whose id is specified
        
        Arguments:
            rideId {String} -- Unique Ride identifier.
        """
        ride  = get_ride(rideId)
        if ride:
            return ride, 200
        return {
            "message":f"Ride:{rideId} Does not exists"
        }, 404


@ride_ns.route("/users/rides/<rideId>", endpoint="update_ride")
class RideUpdate(Resource):
    """Handles ride update endpoint

    PUT /users/rides/<rideId>"""

    update_ride_parser = reqparse.RequestParser()
    update_ride_parser.add_argument('starting_point', type=string_validator,
                                required=True, location='json')
    
    update_ride_parser.add_argument('destination', type=string_validator,
                                required=True, location='json')

    update_ride_parser.add_argument('depart_time', type=date_validator,
                                required=True, location='json')

    update_ride_parser.add_argument('eta', type=date_validator,
                                required=True, location='json')
    
    update_ride_parser.add_argument('seats', type=int,
                                required=True, location='json')
    
    update_ride_parser.add_argument('vehicle', type=string_validator,
                                required=True, location='json')
    
    @ride_ns.doc("update_a_ride", 
        parser=update_ride_parser, 
        params={"rideId": "Unique Ride identifier"},
        security="bearer",
        response={
            404: "Ride to update Not found",
            200: "Ride Update was a sucess",
            401: "User Not allowed to update the ride"
        },
    )
    @jwt_required()
    def put(self, rideId):
        """update Ride details
        
        Arguments:
            rideId {String} -- Unique Ride identifier.
        """
        ride = get_ride(rideId)
        if ride:
            if ride['driver'] in get_jwt_identity():
                update_ride_args = self.update_ride_parser.parse_args()
                update_ride(rideId, **update_ride_args)
                return {
                    "message":"Ride details were update",
                    "ride": url_for("api_Bp.view_ride", rideId=rideId)

                },200
            return {
                "message":"Your do not own the ride"
            }, 401 
        return {
            "message":"Ride:{} Does not exists".format(rideId)
        }, 404


@ride_ns.route("/rides/<rideId>/requests", endpoint="show_interest")
class RideRequest(Resource):
    """Handles the making of a request to join ride

    endpoint: /api/v1/rides/<rideId>/requests
    """
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('destination', type=string_validator,
                            required=True, location='json')
    
    @ride_ns.doc("request_ride", parser=req_parser,
        params={"rideId": "Unique Identifier of a ride"},
        security="bearer",
        response={
            404: "Ride was not found",
            400: "Not allowed to request on ride",
            201: "Request on ride was successful"
        },
    )
    @jwt_required()
    def post(self, rideId):
        """Makes a request to join a ride
        
        Arguments:
            rideID{Integer} -- Unique Identifier of a ride
        """

        req_args = self.req_parser.parse_args()
        ride_to_request = get_ride(rideId)
        passenger = get_jwt_identity()

        if not ride_to_request:
            return {
                "message":f"Ride:{rideId} Does not exists"
            }, 404

        if ride_to_request["driver"] == passenger:
        
            return{
                "message":"You cannot make a request to your own ride"
            }, 400
        
        abort_ride_request_already_made(rideId, passenger)


        reqID = make_request(rideId, passenger, req_args['destination'])

        return{
            "message": "You have requested to join the ride",
            "view_request": '/api/v1/users/rides/{}/requests/{}'.format(rideId, reqID)
        }, 201


@ride_ns.route("/users/rides/<rideId>/requests", endpoint="view_interests")
class RideRequests(Resource):
    """Get all requests on a ride
    endpoint GET /users/rides/<rideId>/requests'
    """

    @ride_ns.doc("ride_requests", 
        params={"rideId": "Unique Ride Identifier"},
        response={
            404: "Ride not found",
            200: "Success requests on a ride retrieved",
            401: "Your not authorized to view requests"
        },
        security="bearer"
    )
    @jwt_required()
    def get(self, rideId):
        """Fetch all requests on a ride
        
        Arguments:
            rideID {String} -- Unique Ride Identifier
        """
        ride  = get_ride(rideId)

        if not ride:
            return {
                "message":f"Ride:{rideId} Does not exists"
            }, 404

        if ride['driver'] == get_jwt_identity():
            # get ride requests
            return get_ride_requests(rideId), 200
        return {
            "message": "Your not authorized to view these requests"
        }, 401


    @ride_ns.doc('retract_request',
        response={
            404: 'Ride does not exist',
            200: 'Success, Request to ride was retracted'
        },
        params={'rideId': 'Unique Indentifier of a ride'},
        security="bearer"
    )
    @jwt_required()
    def delete(self, rideId):
        """Retracts a Request to join a ride
        
        Arguments:
            rideId {String} -- Unique Indentifier of a ride
        """
        ride = get_ride(rideId)

        if not ride:
            return {
                "message":f"Ride:{rideId} Does not exists"
            }, 404

        response = retract_request(rideId, get_jwt_identity())

        return{
            "message": response
        }, 200


# TODO: enable this endpoint to accept and reject endpoints

# @api.route('users/rides/<rideId>requests/<requestId>', 
#             endpoint="request_action")
# class RequestAction(Resource):
#     """Handles Request Action:accept or reject
    
#     endpoint /api/v1/rides/<rideId>/requests/<requestId>
#     """
#     action_parser = reqparse.RequestParser()
#     action_parser.add_argument('action', type=action_validator, 
#                                 location='json', required=True)
    
#     @api.doc("request_action", parser=action_parser,
#         params={
#             "rideId": "Unique Ride Identifier",
#             "requestId": "Unique Request Identifier"
#         },
#         response={
#             404: "Ride or Request Not found",
#             401: "Forbidden to view requests on a ride",
#             200: "Success Action on request",
#             409: "Duplicate Action on request"
#         },
#         security="bearer"
#     )
#     @jwt_required
#     def put(self, rideId, requestId):
#         """Toggles request status: rejected / accepted
#         """

#         if not get_ride(rideId):
            
#             return {
#                 "message":"Ride:{} Does not exists".format(rideId)
#             }, 404

#         ride = get_ride(rideId)
#         if ride['driver'] not in get_jwt_identity():
#             return {
#                 "message": "Your not authorized to view these requests"
#             }, 401
        

#         if abort_request_not_found(requestId):
            
        
#         action_arg = self.action_parser.parse_args()
        
#         req = get_request(requestId)

#         if req['status'] == action_arg['action']:
#             return {
#                 "message": "Ride request has already been '{}'".format(action_arg['action'])
#             }, 409

#         update_request_status(action_arg['action'], requestId) 
#         msg = "Ride Request has been '{}'".format(get_request(requestId)['status'])
#         return {
#             "message":msg
#         }, 200


