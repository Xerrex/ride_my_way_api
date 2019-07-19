"""Defines ride Resources"""
from flask_restplus import Namespace, Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.validators import string_validator, date_validator, action_validator

from app.data.ride_data import create_ride, get_rides,\
    get_ride, make_request, abort_ride_request_found, \
    retract_request, get_ride_requests, \
    abort_request_not_found, get_request, \
    update_request_status, update_ride, abort_active_ride

api = Namespace("Ride", description="Ride operations")



def check_token():
    """Check if there is an active user sssion
    """
    if not get_jwt_identity():
        msg = "You must have an access token",
        link = "/api/v1/auth/login"
        abort(401, message=msg, login_link=link)   


@api.route("rides", endpoint="rides")
class RidesResource(Resource):
    """Handles Rides Resource
    
    endpoint GET /rides
    """
    
    @api.doc('get_all_rides', 
            responses={200: 'Get all rides',
    })
    def get(self):
        """Get all available rides
        """
        return get_rides(), 200


@api.route("rides/<string:rideId>", endpoint="view")
class RideResource(Resource):
    """Handles the ride resources
    
    endpoint: /api/v1/rides/<rideId>
    """
    @api.doc("view_ride", 
        response={
            404: "Ride does not exist",
            200: "Ride was Found"
        },
        params={'rideId': 'Unique Ride identifier'},
        security="bearer"
    )
    @api.header("Authorization", "JWT", required=True)
    @jwt_required
    def get(self,rideId):
        """Gets a rides whose id is specicified
        
        Arguments:
            rideId {String} -- Unique Ride identifier.
        """
        if not get_ride(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        return get_ride(rideId), 200


@api.route("users/rides", endpoint="create")
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

    @api.doc("create_ride", 
        parser=ride_parser, 
        response={
            201: "New ride offer was Created"
        },
        security="bearer"
    )
    @jwt_required
    def post(self):
        """Creates a new ride
        """

        ride_args = self.ride_parser.parse_args()

        abort_active_ride(ride_args['eta'], get_jwt_identity())
        
        ride_id = create_ride(starting_point=ride_args['starting_point'],
                    destination=ride_args['destination'],
                    depart_time=ride_args['depart_time'],
                    eta=ride_args['eta'],
                    vehicle=ride_args['vehicle'],
                    seats=ride_args['seats'],
                    driver=get_jwt_identity())
        
        return {
            "message":"New ride offer was created",
            "view_ride":"/api/v1/rides/{}".format(ride_id)
        }, 201


@api.route("users/rides/<string:rideId>", endpoint="update")
class RideUpdate(Resource):
    """Handles ride update endpoint

    PUT /users/rides/<rideId>"""

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
    
    @api.doc("update_ride", parser=update_parser, 
        response={
            404: "Ride to update Not found",
            200: "Ride Update was a sucess",
            401: "User Not allowed to update the ride"
        },
        params={"rideId": "Unique Ride identifier"},
        security="bearer"
    )
    @jwt_required
    def put(self, rideId):
        """update Ride details
        
        Arguments:
            rideId {String} -- Unique Ride identifier.
        """

        if not get_ride(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        ride = get_ride(rideId)

        if ride['driver'] in get_jwt_identity():
            update_args = self.update_parser.parse_args()
            updated_ride = update_ride(rideId, 
                                starting_point=update_args['starting_point'],
                                destination=update_args['destination'],
                                depart_time=update_args['depart_time'],
                                eta=update_args['eta'],
                                vehicle=update_args['vehicle'],
                                seats=update_args['seats']
                                    )
            return {
                "message":"Ride details were update",
                "ride": updated_ride
            },200
            
        return {
            "message":"Your do not own the ride"
        }, 401 


@api.route("rides/<string:rideId>/requests", endpoint="request")
class RideRequest(Resource):
    """Handles the Ride Requests resources

    endpoint: /api/v1/rides/<rideId>/requests
    """
    req_parser = reqparse.RequestParser()
    req_parser.add_argument('destination', type=string_validator,
                            required=True, location='json')
    
    @api.doc("request_ride", parser=req_parser, 
        response={
            404: "Ride was not found",
            400: "Not allowed to request on ride",
            201: "Request on ride was successful"
        },
        params={"rideId": "Unique Identifier of a ride"},
        security="bearer"
    )
    @jwt_required
    def post(self, rideId):
        """Makes a request to join a ride
        
        Arguments:
            rideId {String} -- Unique Identifier of a ride
        """

        req_args = self.req_parser.parse_args()

        if not get_ride(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        if get_ride(rideId)["driver"] == get_jwt_identity():
        
            return{
                "message":"You cannot make a request to your own ride"
            }, 400
        
        abort_ride_request_found(rideId, get_jwt_identity())

       
        req_id = make_request(rideId, get_jwt_identity(), req_args['destination'])

        return{
            "message": "You have requested to join the ride",
            "view_request": '/api/v1/users/rides/{}/requests/{}'.format(rideId, req_id)
        }, 201

    
    @api.doc('retract_request',
        response={
            404: 'Ride does not exist',
            200: 'Success, Request to ride was retracted'
        },
        params={'rideId': 'Unique Indentifier of a ride'},
        security="bearer"
    )
    @jwt_required
    def delete(self, rideId):
        """Retracts a Request to join a ride
        
        Arguments:
            rideId {String} -- Unique Indentifier of a ride
        """

        if not get_ride(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        response = retract_request(rideId, get_jwt_identity())

        return{
            "message": response
        }, 200


@api.route("users/rides/<string:rideId>/requests", 
            endpoint="requests")
class RideRequests(Resource):
    """Get all requests on a ride
    endpoint GET /users/rides/<rideId>/requests'
    """

    @api.doc("ride_requests", 
        params={"rideId": "Unique Ride Identifier"},
        response={
            404: "Ride not found",
            200: "Success requests on a ride retrieved",
            401: "Your not authorized to view requests"
        },
        security="bearer"
    )
    @jwt_required
    def get(self, rideId):
        """Fetch all requests on a ride
        
        Arguments:
            rideId {String} -- Unique Ride Identifier
        """

        if not get_ride(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        ride = get_ride(rideId)
        if ride['driver'] == get_jwt_identity():
            # get ride requests
            return get_ride_requests(rideId), 200
        return {
            "message": "Your not authorized to view these requests"
        }, 401


@api.route('rides/<string:rideId>requests/<string:requestid>', 
            endpoint="requests_action")
class RequestAction(Resource):
    """Handles Request Action:accept or reject
    
    endpoint /api/v1/rides/<rideId>/requests/<requestId>
    """
    action_parser = reqparse.RequestParser()
    action_parser.add_argument('action', type=action_validator, 
                                location='json', required=True)
    
    @api.doc("request_action", parser=action_parser,
        params={
            "rideId": "Unique Ride Identifier",
            "requestId": "Unique Request Identifier"
        },
        response={
            404: "Ride or Request Not found",
            401: "Forbidden to view requests on a ride",
            200: "Success Action on request",
            409: "Duplicate Action on request"
        },
        security="bearer"
    )
    @jwt_required
    def put(self, rideId, requestId):
        """Toggles request status: rejected / accepted
        """

        if not get_ride(rideId):
            
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        ride = get_ride(rideId)
        if ride['driver'] not in get_jwt_identity():
            return {
                "message": "Your not authorized to view these requests"
            }, 401
        

        if abort_request_not_found(requestId):
            
            return {
                "message": "Request to the ride Does not exist",
                "requests_link":'/api/v1/rides/{}/requests'.format(rideId)
            }, 404
        
        action_arg = self.action_parser.parse_args()
        
        req = get_request(requestId)

        if req['status'] == action_arg['action']:
            return {
                "message": "Ride request has already been '{}'".format(action_arg['action'])
            }, 409

        update_request_status(action_arg['action'], requestId) 
        message = "Ride Request has been '{}'".format(get_request(requestId)['status'])
        return {
            "message":message
        }, 200

    @api.doc("get_request", 
        params={
            "rideId": "Unique Ride Identifier",
            "requestId": "Unique Request Identifier"
        }, 
        response={
            404: "Ride or Request not found",
            401: "Not authorized to view requests",
            200: "Success"
        },
        security="bearer"
    )
    @jwt_required
    def get(self, rideId, requestId):
        """Get a request"""

        if not get_ride(rideId):
            return {
                "message":"Ride:{} Does not exists".format(rideId)
            }, 404

        ride = get_ride(rideId)
        if ride['driver'] not in get_jwt_identity():
            return {
                "message": "Your not authorized to view these request"
            }, 401
        
        if abort_request_not_found(requestId):
            return {
                "message": "Request to the ride Does not exist",
                "requests_link":'/api/v1/rides/{}/requests'.format(rideId)
            }, 404
        
        return get_request(requestId), 200

