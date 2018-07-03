"""Defines Data Models for the aplication"""
from uuid import uuid4
from werkzeug.security import generate_password_hash

from .db import get_db, close_db

class User:
    """Defines the User Data Model"""

    def __init__(self, name, email, password):
        self.id = uuid4().hex
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
    
    def save(self):
        """Saves a New user to the database"""
        
        close_db()
        db = get_db()
        with db.cursor() as cursor:
            query = "INSERT INTO users VALUES (%s, %s, %s, %s)"
            data = (self.id, self.name, self.email, self.password)
            cursor.execute(query, data)
            db.commit()
            db.close()
            

class Ride:
    """Define the Ride Model
    """
    def __init__(self,**kwargs):
        """Create a Ride Instance
        """

        self.starting_point = kwargs['starting_point']
        self.destination = kwargs['destination']
        self.depart_time = kwargs['depart_time']
        self.eta = kwargs['eta']
        self.seats = kwargs['seats']
        self.vehicle = kwargs['vehicle']
        self.driver = kwargs['driver']
    
    def save(self):
        
        close_db()
        db = get_db()
        with db.cursor() as cursor:
            fields = "(starting_point, destination, depart_time, \
            eta, seats, vehicle, driver)"
            query = "INSERT INTO rides " + fields + "\
             VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"
            data = (self.starting_point, self.destination, self.depart_time, 
                    self.eta, self.seats, self.vehicle, self.driver
            )
            cursor.execute(query, data)
            ride_id = cursor.fetchone()[0]
            db.commit()
            db.close()

            return ride_id


class RideRequest:
    """Defines a Ride_request
    """

    def __init__(self, ride, user, destination, ):
        """Create a new Ride_Request Instance
        
        Arguments:
            ride {String} -- Unique Ride Identifier
            user {String} -- Unique User Identifier
            destination {String} -- Town the User is headed to.
        """

        self.user = user
        self.destination = destination
        self.ride = ride
        self.status = "" # toggle: acccepted/rejected
    
    def save(self):
        """saves a newly created ride request
        """
        fields = "(ride_id, user_id, destination, req_status)"
        query = "INSERT INTO requests " + fields + " VALUES (%s, %s, %s, %s) RETURNING id"
        data = (self.ride, self.user, self.destination, self.status)

        close_db()
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute(query, data)
            req_id = cursor.fetchone()[0]
            db.commit()
            db.close()

            return req_id
        
    
