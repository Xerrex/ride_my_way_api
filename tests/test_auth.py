from unittest import main
import json


from app import create_app
from app.db import initialize, get_db, close_db
from basetest import TestBase


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

        with self.app.test_request_context():
            close_db()
            initialize() # create all tables

    def tearDown(self):
        
        with self.app.test_request_context():
            close_db()
            db = get_db()
            # Drop all the tables
            cursor = db.cursor()
            cursor.execute("DROP TABLE users")
            cursor.execute("DROP TABLE rides")
            cursor.execute("DROP TABLE requests")
            db.commit()
            cursor.close()
            db.close()
            
        self.client.post('/api/v1/auth/logout', content_type='application/json')
        self.app = None
        self.client = None

    def register(self):
        """Create new users
        """

        response = self.client.post('/api/v1/auth/register', 
                                    data=json.dumps(self.test_user), 
                                    content_type='application/json')
        return response
    
    def login(self):
        """Starts a user session
        """
        response = self.client.post('/api/v1/auth/login', 
                                    data=json.dumps(self.test_login), 
                                    content_type='application/json')
        return response


    def test_user_registration(self):
        """Test user can registration

        Assert that a valid POST request to /api/v1/auth/register
        registers a new user
        """

        response = self.register()

        self.assert201(response)

        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn("User Account Was Created Successfully.", response_data['message'])
    

    def test_user_log_in(self):
        """Test user can login

        Assert that a valid POST request to /api/v1/auth/login
        starts a User session:
        """

        self.register()
                                    
        response = self.login()
        
        self.assert200(response)

        data = json.loads(response.get_data(as_text=True))

        self.assertIn(self.test_user['name'], data['message'])

    def test_duplicate_user_registration(self):
        """Test user cannot register twice

        Assert that a valid POST request to /api/v1/auth/register
        twice with same data fails with 409 status code
        """

        self.register()
        
        response = self.register()
        
        self.assert409(response)

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertIn(message, 'User with that email already exists.')

    def test_user_is_already_logged_in(self):
        """Test user cannot logged twice

        Assert that a valid Post request to /api/v1/auth/login
        when a user is already logged in fails with 409
        """

        self.register()

        self.login()

        response = self.login()

        self.assert409(response)

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual("Make sure to logout first", message)

    def test_non_registered_user_login(self):
        """Test user cannot login if not registered

        Assert that a valid POST request to /api/v1/auth/login
        """

        response = self.login()
        
        self.assert401(response)

        expected_msg = "Your email or password is invalid.Please register first"
        msg = json.loads(response.get_data(as_text=True))['message']
        self.assertIn(expected_msg, msg)

    def test_user_can_logout(self):
        """Test user can logout

        Assert that a valid POST Request to /api/v1/auth/logout
        Ends the current user session
        """

        self.register()

        self.login()

        response = self.client.post('/api/v1/auth/logout',
                                    content_type='application/json')

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual("User Session was successfully ended", message)


    def test_logout_for_logged_in_user(self):
        """Test user can logout only if logged in

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




