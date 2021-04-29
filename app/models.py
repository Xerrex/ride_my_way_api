"""Defines Data Models for the aplication"""
from enum import unique
from uuid import uuid4
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash

from .extensions import db

from .db import get_db, close_db # TODO replace with ORM



class User(db.Model):
    """Defines the User Data Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(256))
    rides = db.relationship('Ride', backref='owner', lazy='dynamic')
    interests = db.relationship('Interest', backref='passenger', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def save(self):
        """Saves to the database a new user or update
        """
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}'


class Ride(db.Model):
    """Define the Ride Model
    """
    id = db.Column(db.Integer, primary_key=True)
    start_point = db.Column(db.String(128), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    depart_time = db.Column(db.DateTime, nullable=False)
    et_arrival = db.Column(db.DateTime, nullable=False)
    vehicle_plate = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seats_no = db.Column(db.Integer, nullable=False)
    interests = db.relationship('Interest', backref='ride', lazy='dynamic')

    def __init__(self, owner, **ride_details):
        """Create a Ride Instance
        """

        self.start_point = ride_details['starting_point']
        self.destination = ride_details['destination']
        self.depart_time = ride_details['depart_time']
        self.et_arrival = ride_details['eta']
        self.vehicle_plate = ride_details['vehicle']
        self.user_id = owner
        self.seats_no = ride_details['seats']
        
    
    def save(self):
        """Saves to the database a new ride or update
        """
        db.session.add(self)
        db.commit()

    def __repr__(self):
        return f'<Ride {self.destination} {self.depart_time}>'


class Interest(db.Model):
    """Defines a Ride_request
    """
    id = db.Column(db.Integer, primary_key=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    destination = db.Column( db.String(128), nullable=False)
    status = db.Column(db.String(128), default='pending')

    def __init__(self, rideID, passenger, dest):
        """Create a new Ride_Request Instance
        
        Arguments:
            rideID (String) -- Unique Ride Identifier
            passenger (id) -- Unique User Identifier joining the ride
            dest (String) -- Town the passenger is headed to.
        """
        self.ride_id = rideID
        self.user_id = passenger
        self.destination = dest
    
    def save(self):
        """saves to the database a new ride 
            request or update
        """
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<Interest {self.destination} {self.status}>'

