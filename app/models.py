"""Defines Data Models for the aplication"""
from uuid import uuid4
from werkzeug.security import generate_password_hash

from .db import get_db, commit_db, close_db

class User:
    """Defines the User Data Model"""

    def __init__(self, name, email, password):
        self.id = uuid4().hex
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
    
    def save(self):
        """Saves a New user to the database"""
        
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

class RideRequest:
    """Defines a Ride_request
    """

    def __init__(self, user, destination, ride):
        """Create a new Ride_Request Instance
        
        Arguments:
            user {String} -- Unique User Identifier
            destination {String} -- Town the User is headed to.
            ride {String} -- Unique Ride Identifier
        """
        self.user = user
        self.destination = destination
        self.ride = ride
        self.status = "" # toggle: acccepted/rejected
        
    
