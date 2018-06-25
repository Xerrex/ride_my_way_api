"""Defines the Authentication Resources"""
from flask_restful import Resource, reqparse

from app.validators import string_validator, email_validator, length_validator
from app.data.user_data import create_user, abort_if_user_found

class RegisterResource(Resource):
    """Handles the User Registration endpoint
    """
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('name', type=string_validator,
                                    required=True,location='json')

    user_parser.add_argument('email', type=email_validator,
                                    required=True,location='json')

    user_parser.add_argument('password', type=length_validator,
                                    required=True,location='json')                                                                

    def post(self):
        """Creates a new user
        """

        user_args = self.user_parser.parse_args()

        email = user_args['email']
        abort_if_user_found(email)

        name = user_args['name']
        password = user_args['password']

        create_user(name, email, password)

        
