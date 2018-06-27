"""Define Ride Data container and Data fetching methods
"""
from datetime import datetime, timedelta
from flask_restful import abort

from app.models import Ride, RideRequest

RIDES = {}

REQUESTS = {}


def create_ride(**kwargs):
    """Create a new ride
    """

    ride = Ride(starting_point=kwargs['starting_point'],
            destination=kwargs['destination'],
            depart_time=kwargs['depart_time'],
            eta=kwargs['eta'],
            vehicle=kwargs['vehicle'],
            seats=kwargs['seats'],
            driver=kwargs['driver'])
    
    ride_id = "ride{}".format(len(RIDES)+1)

    RIDES[ride_id] = ride.__dict__

    return [ride_id, ride.__dict__]


def update_ride(ride_id, **kwargs):
    """update a ride"""
    ride = RIDES[ride_id]
    ride['starting_point'] = kwargs['starting_point']
    ride['destination'] = kwargs['destination']
    ride['depart_time'] = kwargs['depart_time']
    ride['eta'] = kwargs['eta']
    ride['vehicle'] = kwargs['vehicle']
    ride['seats'] = kwargs['seats']

    return [ride_id, ride]


def get_rides():
    """Get all avalaible ride offers
    """
    return RIDES


def get_ride(rideId):
    """Get a ride with the Id:rideId
    """
    return RIDES[rideId]


def make_request(user, destination, ride):
    """Make a request to Join a ride
    
    Arguments:
        user {String} -- Unique User Identifier
        destination {String} -- Town the User is headed to.
        ride {String} -- Unique Ride Identifier
    """
    req = RideRequest(user, destination, ride)

    req_id = "req{}".format(len(REQUESTS)+1)
    REQUESTS[req_id] = req.__dict__
    
    return [req_id, req.__dict__]


def retract_request(user, ride):
    """Retracts user request to join a ride
    
    Arguments:
        user {String} -- Unique User Identifier
        ride {String} -- Unique Ride Identifier
    """
    for k,v in REQUESTS.items():
        if v['user']==user and v['ride']==ride:
            del REQUESTS[k]
            return "You have retracted request to join ride"


def get_ride_requests(ride_id):	
    """Get requests made on a ride.
    
    Arguments:
        ride_id {String} -- Unique ride Indentifier
    """
    ride_reqs = {}
    for k, v in REQUESTS.items():
        if v['ride'] == ride_id:
            ride_reqs[k] = v
    return ride_reqs        


def get_request(reqId):
    """Fetch a ride 
    
    Arguments:
        reqId {String} -- Unique request identifier
    """
    return REQUESTS[reqId]

def update_request_status(status, requestID):
    """Update ride request status
    
    Arguments:
        status {String} -- should be 'accepted' or 'rejected'
        requestID {String} -- Unique request identifier
    """
    REQUESTS[requestID]['status'] = status

# #####################################Helpers##################################################

"""Defines Ride helper Methods
"""


def rides_generator(number):
    """Generate rides
    
    Arguments:
        number {Integer} -- Number of rides you want to create
    """
    
    for x in range(1,number+1):
        current_date = datetime.now()
        depart_time = current_date + timedelta(days=x)
        depart_time = depart_time.strftime("%d-%m-%Y %H:%M")

        eta = current_date + timedelta(days=x+1)
        eta = eta.strftime("%d-%m-%Y %H:%M")

        create_ride(starting_point="town{}-meetingplace{}".format(x,x),
                    destination="town{}".format(x+1),
                    depart_time=depart_time,
                    eta=eta,
                    vehicle="KCH {}{}7b".format(x,x+3),
                    seats=5,
                    driver="user{}".format(x))


def abort_ride_not_found(ride):
    
    if ride not in RIDES.keys():
        return None
    return "Ride exists"


def abort_ride_request_found(ride, user):
    """Abort with 409
    
    Arguments:
        user {String} -- Unique User Identifier
        ride {String} -- Unique Ride Identifier
    """

    for v in REQUESTS.values():
        if v['ride']==ride and v['user']==user:
            msg="You have already made a request to join ride"
            abort(409, message=msg)

def abort_request_not_found(reqId):
    """Abort if Ride not found
    
    Arguments:
        reqId {String} -- Unique ride identifier
    """
    if reqId not in REQUESTS.keys():
        return None
    return "request exists"

