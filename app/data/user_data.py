"""Defines user Data Container & fetching methods 
"""
from app.models import User


# User data container
USERS = {}

def create_user(name, email, password):
    """Creates a New user and saves it into container
    
    Arguments:
        name {String} -- User's  full name
        email {String:email} -- User's email
        password {String} -- User password that is not hashed
    """
    user = User(name, email, password)

    user_id = 'user%i'%len(USERS)+1

    USERS[user_id] = user.__dict__

    return{
        "message":"User Account Was Created Successfully.",
        "login_link":"/api/v1/auth/login"
    }, 201

def abort_if_user_found(email):
    """email
    
    Arguments:
        email {String:email} -- User email
    """
    for user in USERS.values():
        if user['email'] == email:
            return {
                "message": "User with that email already exists"
            }, 409
