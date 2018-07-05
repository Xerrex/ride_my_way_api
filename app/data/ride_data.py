"""Define Ride Data container and Data fetching methods
"""
from datetime import datetime, timedelta
from flask_restful import abort

from app.models import Ride, RideRequest
from app.db import get_db, close_db



def create_ride(**kwargs):
    """Create a new ride
    """
    ride = Ride(**kwargs)

    ride_id = ride.save()
    
    return ride_id


def update_ride(ride_id, **kwargs):
    """update a ride"""
    query = """UPDATE rides
                SET starting_point=%s,
                destination=%s,
                depart_time=%s,
                eta=%s,
                vehicle=%s,
                seats=%s
                WHERE id=%s
                RETURNING starting_point,
                destination,
                depart_time,
                eta,
                seats,
                vehicle"""
    data = (
        kwargs['starting_point'],
        kwargs['destination'],
        kwargs['depart_time'],
        kwargs['eta'],
        kwargs['vehicle'],
        kwargs['seats'],
        ride_id
    ) 

    close_db()
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(query, data)
        row = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        
    return {
        "starting_point": row[0],
        "destination": row[1],
        "depart_rime": row[2],
        "eta": row[3],
        "seats": row[4],
        "vehicle": row[5]
    }


def get_rides():
    """Get all avalaible ride offers
    """
    close_db()
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM rides")
        rows = cursor.fetchall()
        cursor.close()
        db.close()

    rides = {}   
    for row in rows:
        ride = {
            "starting_point":row[1],
            "destination":row[2],
            "depart_time":row[3],
            "eta":row[4],
            "vehicle":row[5],
            "seats": row[6]
        }
        rides[row[0]] = ride
            

    return rides


def get_ride(rideId):
    """Get a ride with the Id:rideId
    """
    close_db()
    db = get_db()
    with db.cursor() as cursor:
        query = "SELECT * FROM rides WHERE id=%s"
        cursor.execute(query, (rideId,))
        row = cursor.fetchone()
        cursor.close()
        db.close()

    if row:
        ride = {
                "starting_point":row[1],
                "destination":row[2],
                "depart_time":row[3],
                "eta":row[4],
                "seats":row[5],
                "vehicle": row[6],
                "driver": row[7]
            }    
        return ride
    return


def make_request(ride, user, destination):
    """Make a: request to Join a ride
    
    Arguments
        ride {Integer} -- Unique Ride Identifier
        user {Uuid} -- Unique User Identifier
        destination {String} -- Town the User is headed to.
    """
    ride_request = RideRequest(ride, user, destination)
    req_id = ride_request.save()
    
    return req_id


def retract_request(ride, user):
    """Retracts user request to join a ride
    
    Arguments:
        ride {Integer} -- Unique Ride Identifier
        user {Uuid} -- Unique User Identifier
    """
    close_db()
    db = get_db()
    with db.cursor() as cursor:
        query = "DELETE FROM requests WHERE ride_id=%s AND user_id=%s"
        cursor.execute(query, (ride, user))
        db.commit()
        cursor.close()
        db.close()
        return "You have retracted request to join ride" 


def get_ride_requests(ride_id):	
    """Get requests made on a ride.
    
    Arguments:
        ride_id {String} -- Unique ride Indentifier
    """
    close_db()
    db = get_db()
    query = "SELECT * FROM requests WHERE ride_id=%s"
    with db.cursor() as cursor:
        cursor.execute(query,(ride_id,))
        rows = cursor.fetchall()
        cursor.close()
        db.close() 
    
    ride_reqs = {}
    for row in rows:
        req = {
            "user": row[2],
            "destination": row[3],
            "status": row[4]
        }
        ride_reqs[row[1]] = req
    return ride_reqs        


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


def abort_ride_request_found(ride, user):
    """Abort with 409
    
    Arguments:
        user {String} -- Unique User Identifier
        ride {String} -- Unique Ride Identifier
    """
    close_db()
    db = get_db()
    with db.cursor() as cursor:
        query = "SELECT * FROM requests WHERE ride_id=%s AND user_id=%s"
        cursor.execute(query, (ride, user))
        row = cursor.fetchone()
        cursor.close()
        db.close()

    if row:
        msg="You have already made a request to join ride"
        abort(409, message=msg)   


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

