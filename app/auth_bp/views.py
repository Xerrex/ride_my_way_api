"""Defines the Authentication Resources"""
from flask import session
from flask_restful import Resource, reqparse

from app.validators import string_validator, email_validator, length_validator

from app.data.user_data import create_user, abort_if_user_found, \
abort_user_not_found, get_user_by_email, verify_password

class RegisterResource(Resource):
    """Handles the User Registration 
    
    endpoint: /register
    """
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('name', type=string_validator,
                                    required=True,location='json')

    user_parser.add_argument('email', type=email_validator,
                                    required=True, location='json')

    user_parser.add_argument('password', type=length_validator,
                                    required=True, location='json')                                                                

    def post(self):
        """Creates a new user
        """

        user_args = self.user_parser.parse_args()

        email = user_args['email']
        abort_if_user_found(email)

        name = user_args['name']
        password = user_args['password']

        create_user(name, email, password)

        return{
            "message":"User Account Was Created Successfully.",
            "login_link":"/api/v1/auth/login"
        }, 201


class LoginResource(Resource):
    """Handles User Login 
    
    endpoint: /login
    """

    login_parser = reqparse.RequestParser()
    login_parser.add_argument('email', type=email_validator, 
                                required=True, location='json')

    login_parser.add_argument('password', type=length_validator, 
                                required=True, location='json')

    def post(self):
        """Starts a User session
        """
        login_args = self.login_parser.parse_args()

        email = login_args['email']

        user = get_user_by_email(email)

        if user and verify_password(user[1]['password'], login_args['password']):
            # login user
            if 'userID' not in session:
                session['userID'] = user[0]

                return{
                    "message":"Welcome back {}.".format(user[1]['name'])
                }, 200

            return {
                "message": "Make sure to logout first",
                "logout_link": "/api/v1/auth/logout"
                }, 409

        return {
            "message":"Your email or password is invalid.Please register first",
            "login_link": "/api/v1/auth/register"
            }, 401    


class LogoutResource(Resource):
    """Handles User logout
    
    endpoint: /logout
    """

    def post(self):
        """Ends user session
        """
        if 'userID' in session:
            session.pop('userID', None)
            return {
                "message":"User Session was successfully ended"
            }, 200

        return {
            "message": "You must be logged In to logout",
            "login_link": "/api/v1/auth/login"
            }, 403 
   







        
