"""Defines the Authentication Resources"""
from flask import session
from flask_restplus import Namespace, Resource, reqparse, fields
from flask_jwt_extended import create_access_token

from app.validators import string_validator, email_validator, length_validator

from app.data.user_data import create_user, abort_if_user_found, \
get_user_by_email, verify_password

api = Namespace('Authentication', description="Authentication Operations")

new_user= api.model("New_user",{
    "name": fields.String(required=True, description='name of the new user'),
    "email": fields.String(required=True, description='email of the new user'),
    "password": fields.String(required=True, description='password for the new user')
})

@api.route('/register', endpoint="register")
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

    @api.doc('create_user',parser=user_parser, 
                 responses={201: 'user account created successfully'})
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


@api.route('/login', endpoint="login")
class LoginResource(Resource):
    """Handles User Login 
    
    endpoint: /login
    """

    login_parser = reqparse.RequestParser()
    login_parser.add_argument('email', type=email_validator, 
                                required=True, location='json')

    login_parser.add_argument('password', type=length_validator, 
                                required=True, location='json')

    @api.doc('user_login',parser=login_parser, 
        responses={
            200: 'Welcome User back',
            409: 'Inform User to logout first',
            401: 'Invalid login credentials'
        })
    @api.expect(login_parser)
    def post(self):
        """Starts a User session
        """
        login_args = self.login_parser.parse_args()

        email = login_args['email']

        user = get_user_by_email(email)

        if user and verify_password(user[3], login_args['password']):
            # login user
            if 'userID' not in session:
                session['userID'] = user[0]

                return{
                    "message":"Welcome back '{}'.".format(user[1]),
                    "access_token":create_access_token(identity=user[0])
                }, 200

            return {
                "message": "Make sure to logout first",
                "logout_link": "/api/v1/auth/logout"
                }, 409

        return {
            "message":"Your email or password is invalid.Please register first",
            "login_link": "/api/v1/auth/register"
            }, 401    


@api.route('/logout', endpoint="logout")
class LogoutResource(Resource):
    """Handles User logout
    
    endpoint: /logout
    """
    @api.doc('logout_user', 
            responses={
                200: 'User Session was successfully ended',
                403: "Logout is Forbidden. Login is needed first"
            })
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

