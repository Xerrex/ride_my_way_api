"""Defines user Data Container & fetching methods 
"""
from werkzeug.security import check_password_hash
from flask_restful import abort
from app.models import User
from app.db import get_db


def create_user(name, email, password):
    """Creates a New user and saves it into container
    
    Arguments:
        name {String} -- User's  full name
        email {String:email} -- User's email
        password {String} -- User password that is not hashed
    """
    user = User(name, email, password)
    user.save()


def get_user_by_email(email):
    """Get a user by their email
    
    Arguments:
        email {String:email}
    """
    # for user_id in USERS.keys():
    #     if USERS[user_id]['email'] == email:
    #         return [user_id,USERS[user_id]]
    # return 
    db = get_db()
    with db.cursor() as cursor:
        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
    if user:
        return user
    return None 


def verify_password(password_hash, password):
    """Verify User passwor against its hash
    
    Arguments:
        password_hash {hash} -- Hash generated by 
                                werkzeug.security generate_password_hash
        password {String} -- Unhashed User password
    """
    return check_password_hash(password_hash, password)

    
def abort_if_user_found(email):
    """Abort with 409 status code
    
    Arguments:
        email {String:email} -- User email
    """
    # for user in USERS.values():
    #     if user['email'] == email:
    #         abort(409, message="User with that email already exists")

    db = get_db()
    with db.cursor() as cursor:
        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
    if user:
       abort(409, message="User with that email already exists")     

        

