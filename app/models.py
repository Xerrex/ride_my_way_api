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
        
        db = get_db()
        query = "INSERT INTO users (id, name, email, password) VALUES(?,?,?,?)"
        data = (self.id, self.name, self.email, self.password)
        db.execute(query, data)
        db.commit()
        close_db()


class Ride:
    """Define the Ride Model
    """
    def __init__(self,driver, **ride_details):
        """Create a Ride Instance
        """

        self.starting_point = ride_details['starting_point']
        self.destination = ride_details['destination']
        self.depart_time = ride_details['depart_time']
        self.eta = ride_details['eta']
        self.seats = ride_details['seats']
        self.vehicle = ride_details['vehicle']
        self.driver = driver
    
    def save(self):
        """Saves a new ride to the database"""
        
        db = get_db()
        fields = "(starting_point, destination, depart_time, \
        eta, seats, vehicle, driver)"
        query = "INSERT INTO rides " + fields + "\
            VALUES (?, ?, ?, ?, ?, ?, ?)"
        data = (self.starting_point, self.destination, self.depart_time, 
                    self.eta, self.seats, self.vehicle, self.driver)
        
        cursor = db.cursor()
        cursor.execute(query, data)
        db.commit()
        ride_id = cursor.lastrowid
        cursor.close()
        close_db()

        return ride_id


class RideRequest:
    """Defines a Ride_request
    """

    def __init__(self, rideID, passenger, dest):
        """Create a new Ride_Request Instance
        
        Arguments:
            rideID (String) -- Unique Ride Identifier
            passenger (Uuid) -- Unique User Identifier wishing to join the ride
            destination (String) -- Town the passenger is headed to.
        """

        self.ride = rideID
        self.passenger = passenger
        self.destination = dest
        self.status = "" # toggle: accepted/rejected
    
    def save(self):
        """saves a newly created ride request
        """
        fields = "(ride_id, user_id, destination, req_status)"
        query = f"INSERT INTO requests {fields} VALUES (?,?,?,?)"
        data = (self.ride, self.passenger, self.destination, self.status)

        db = get_db()
        cursor = db.cursor()
        cursor.execute(query, data)
        db.commit()
        reqID = cursor.lastrowid
        cursor.close()
        close_db()

        return reqID
        
    
