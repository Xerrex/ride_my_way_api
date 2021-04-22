"""Define Ride Data container and Data fetching methods
"""
from datetime import datetime, timedelta
from flask_restplus import abort

from app.models import Ride, RideRequest
from app.db import get_db, close_db



def create_ride(driver, **ride_details):
    """Create a new ride to be shared

    Args:
        driver (UUID): A Unique identifier of owner of the ride
        ride_details(KeyWord Args): Details of the ride to be shared

    Returns:
        rideID: the id of the created ride.
    """

    ride = Ride(driver, **ride_details)

    rideID = ride.save()
    
    return rideID


def get_rides():
    """Get all avalaible ride offers
    """
    
    db = get_db()
    ride_rows = db.execute("SELECT * FROM rides").fetchall()
    close_db()

    rides = {}   
    for ride in ride_rows:
        rides[ride[0]] = dict(ride)
            

    return rides


def get_ride(rideID):
    """Get a ride with the id:rideID

    Args:
        rideID (Integer): Unique Identifier of a ride

    Returns:
        dict: contians a fetched ride details
    """
    db = get_db()
    query = "SELECT * FROM rides WHERE id=?"
    ride = db.execute(query, (rideID,)).fetchone()
    close_db()

    if ride:   
        return dict(ride)
    return


def update_ride(rideID, **ride_details):
    """update a ride
    
    Args:
        rideID (Integer): Unique Identifier of a ride
        **ride_details (Keyword args): keyword values of a rides details
    """
    
    query = """UPDATE rides
        SET starting_point=?, destination=?,
        depart_time=?, eta=?, vehicle=?,
        seats=?
        WHERE id=?
        """
    data = (
        ride_details['starting_point'], 
        ride_details['destination'],
        ride_details['depart_time'], 
        ride_details['eta'], 
        ride_details['vehicle'],
        ride_details['seats'], 
        rideID
    ) 
    db = get_db()
    db.execute(query, data)
    close_db()
    return 


def make_request(rideID, passenger, dest):
    """Make a: request to Join a ride
    
    Arguments
        rideID{Integer} -- Unique Ride Identifier
        passenger {Uuid} -- Unique User  Identifier
        dest {String} -- Town the User is headed to
    
    Returns:
        Integer : contains id of the request
    """
    ride_req = RideRequest(rideID, passenger, dest)
    req_id = ride_req.save()
    
    return req_id


def retract_request(ride, user):
    """Retracts user request to join a ride
    
    Arguments:
        ride {Integer} -- Unique Ride Identifier
        user {Uuid} -- Unique User Identifier
    """
    
    db = get_db()
    query = "DELETE FROM requests WHERE ride_id=? AND user_id=?"
    db.execute(query, (ride, user))
    db.commit()
    close_db()
    return "You have retracted request to join ride" 


def get_ride_requests(rideID):
    """Get requests made on a ride.
    
    Arguments:
        rideID {String} -- Unique ride Indentifier
    """
    
    db = get_db()
    query = "SELECT * FROM requests WHERE ride_id=?"
    ride_reqs = db.execute(query, rideID).fetchall()
    close_db()

    ride_requests = {} 
    for ride_req in ride_reqs:
        req = {
            "passenger": ride_req[2],
            "destination": ride_req[3],
            "status": ride_req[4]
        }
        ride_requests[ride_req[1]] = req
    
    return ride_requests      


def get_request(reqId):
    """Fetch a ride 
    
    Arguments:
        reqId {String} -- Unique request identifier
    """
    query = "SELECT * FROM requests WHERE id=%s"
    close_db()
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, (reqId,))
        row = cursor.fetchone()
        cursor.close()
        db.close()
    req = {
        "user": row[2],
        "destination":row[3],
        "status": row[4]
    }    

    return req


def update_request_status(status, requestID):
    """Update ride request status
    
    Arguments:
        status {String} -- should be 'accepted' or 'rejected'
        requestID {String} -- Unique request identifier
    """
    query = "UPDATE requests SET req_status=%s WHERE id=%s"

    close_db()
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query,(status,requestID))
        db.commit()
        cursor.close()
        db.close()


# #####################################Helpers##################################################

"""Defines Ride helper Methods
"""

def abort_ride_request_already_made(rideID, passenger):
    """Abort with 409
    
    Arguments:
        rideID {Integer} -- Unique Identifier of ride ID
        passenger {String} -- Unique Identifier of passenger joining ride
    """

    db = get_db()
    query = "SELECT * FROM requests WHERE ride_id=? AND user_id=?"
    ride_request = db.execute(query, (rideID, passenger)).fetchone()
    close_db()
    
    if ride_request:
        msg="You have already made a request to join this ride"
        abort(409, msg)   


def abort_request_not_found(reqId):
    """Abort if Ride not found
    
    Arguments:
        reqId {String} -- Unique ride identifier
    """
    query = "SELECT * FROM requests WHERE id={}".format(reqId)
    close_db()
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query)
        req = cursor.fetchone()
        cursor.close()
        db.close()
    if not req:
        return "yes do abort"
    return     


def abort_active_ride(depart_time, ride_creator):
    """Abort if User has an uncompleted ride 
    
    Arguments:
        depart_time {Datetime} -- depart time of a ride.
        ride_creator {Uuid} -- Unique identifier of person creating ride.
    """

    query = "SELECT * FROM rides WHERE eta<=? AND driver=?"
    db =get_db()
    ride = db.execute(query,(depart_time, ride_creator)).fetchone()
    close_db()
    
    if ride:
        eta = dict(ride)["eta"]
        err = f"You have an uncompleted ride that before-{eta}"
        msg = f"Create a ride after- {eta}"
        abort(409, msg, error=err)

