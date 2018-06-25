"""Defines Data Models for the aplication"""
from werkzeug.security import generate_password_hash


class User:
    """Defines the User Data Model"""

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
    
