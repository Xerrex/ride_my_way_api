from unittest import main
import json

from flask import url_for

from app import create_app
from app.data.user_data import USERS

from . import TestBase


class AuthCase(TestBase):
    """Defines Tests for user Authentication
    """

    test_user = {
        "name": "Bob alice",
        "email": "bobalice@dev.com",
        "password": "12345dfgh"
    }

    test_login = {
        "email": "bobalice@dev.com",
        "password": "12345dfgh"
    }

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()


    def tearDown(self):
        self.client.post('/api/v1/auth/logout', content_type='application/json')
        USERS.clear()

        self.app = None
        self.client = None

    def test_user_registration(self):
        """Test user registration

        Assert that a valid POST request to /api/v1/auth/register
        registers a new user
        """

        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')

        self.assert201(response)

        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("User Account Was Created Successfully.", response_data['message'])
    
    def test_user_log_in(self):
        """Test user login

        Assert that a valid POST request to /api/v1/auth/login
        starts a User session:
        """

        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')
                                    
        response = self.client.post('/api/v1/auth/login', 
                                    data=json.dumps(self.test_login), 
                                    content_type='application/json')
        
        self.assert200(response)

        data = json.loads(response.get_data(as_text=True))

        self.assertIn(self.test_user['name'], data['message'])

    def test_duplicate_user_registration(self):
        """Test duplicate User Registration

        Assert that a valid POST request to /api/v1/auth/register
        twice with same data fails with 409 status code
        """

        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')
        
        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')
        
        self.assert409(response)

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertIn(message, 'User with that email already exists.')

    def test_user_is_already_logged_in(self):
        """Test User is already already logged in

        Assert that a valid Post request to /api/v1/auth/login
        when a user is already logged in fails with 409
        """

        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')

        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.test_login),
                                    content_type='application/json')

        response = self.client.post('/api/v1/auth/login', 
                                    data=json.dumps(self.test_login),
                                    content_type='application/json')

        self.assert409(response)

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual("Make sure to logout first", message)

    def test_non_registered_user_login(self):
        """Test login for a user that is not registered

        Assert that a valid POST request to /api/v1/auth/login
        """

        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.test_login),
                                    content_type='application/json')
        
        self.assert401(response)

        expected_msg = "Your email or password is invalid.Please register first"
        msg = json.loads(response.get_data(as_text=True))['message']
        self.assertIn(expected_msg, msg)

    def test_user_can_logout(self):
        """Test logout

        Assert that a valid POST Request to /api/v1/auth/logout
        Ends the current user session
        """

        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')

        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(self.test_login),
                                    content_type='application/json')

        response = self.client.post('/api/v1/auth/logout',
                                    content_type='application/json')

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual("User Session was successfully ended", message)


    def test_logout_for_logged_in_user(self):
        """Test that only logged in user can logout

        Assert that a POST Request to /api/v1/auth/logout
        fails if user is not logged in.
        """
        response = self.client.post('/api/v1/auth/logout',
                                    content_type='application/json')
        self.assert403(response)                          

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual("You must be logged In to logout", message)


if __name__ == "__main__":
    main(verbosity=2)




