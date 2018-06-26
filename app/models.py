"""Defines Data Models for the aplication"""
from werkzeug.security import generate_password_hash


class User:
    """Defines the User Data Model"""

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)


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
        
    
