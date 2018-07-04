from unittest import main
import json
from datetime import datetime, timedelta

from app import create_app
from app.db import initialize, close_db, get_db
from basetest import TestBase

class RideCase(TestBase):
    """Contains tests on a ride and requests made on ride.
    """
    current_date = datetime.now() + timedelta(days=1)
    eta = current_date + timedelta(days=1)
    
    test_ride = {
        "starting_point": "Nairobi-Kencom",
        "destination": "Taita-wunda",
        "depart_time": "{}".format(current_date.strftime("%d-%m-%Y %H:%M")),
        "eta": "{}".format(eta.strftime("%d-%m-%Y %H:%M")),
        "seats": "",
        "vehicle": "KCH 001"
    }

    ride_user = {
        "name": "Bob Rider",
        "email": "bobrider@dev.com",
        "password": "12345dfgh"
    }

    ride_pass = {
        "name": "Bob Pass",
        "email": "bobpass@dev.com",
        "password": "12345dfghqwyn"
    }

    rider_login = {
        "email": "bobrider@dev.com",
        "password": "12345dfgh"
    }

    pass_login = {
        "email": "bobpass@dev.com",
        "password": "12345dfghqwyn"
    }

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()

        with self.app.test_request_context():
            close_db()
            initialize() # create all tables

        # create User
        self.client.post('/api/v1/auth/register', 
                            data=json.dumps(self.ride_user), 
                            content_type='application/json')
        
        # login user
        self.client.post('/api/v1/auth/login', 
                            data=json.dumps(self.rider_login), 
                            content_type='application/json')
    
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

    def create_ride(self, seats):
        """create a new ride
        """
        self.test_ride["seats"] = seats
        test_ride = self.test_ride
        response = self.client.post('/api/v1/users/rides', data=json.dumps(test_ride), 
                                    content_type='application/json')
        
        return response

    def test_ride_creation(self):
        """Test user can create a ride offer

        Assert that a valid POST request to /api/v1/users/rides
        Creates a new ride.    
        """
        response = self.create_ride(4)
        self.assert201(response)
    
    def test_get_available_rides(self):
        """Test user can view all available rides

        Assert that a valid GET request to /api/v1/rides
        returns all available rides
        """
        response = self.client.get('api/v1/rides', content_type='application/json')
        
        self.assert200(response)
    
    def test_get_a_specific_ride(self):
        """Test user can view a specific ride

        Assert that a valid GET request to /api/v1/rides/<rideId>
        returns a specific ride
        """

        response = self.create_ride(4)

        self.assert201(response)

        data = json.loads(response.get_data(as_text=True))     
        response = self.client.get(data['view_ride'], content_type='application/json')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(self.test_ride['starting_point'], data['starting_point'])

    def test_ride_details_update(self):
        """Test user can update details

        Assert that a valid PUT request to /api/v1/users/rides/<rideId>
        updates the ride details.
        """

        response = self.create_ride(10)
                                
        ride_update = {
            "starting_point": "Nairobi-Kencom",
            "destination": "Taita-wunda",
            "depart_time": "{}".format(self.current_date.strftime("%d-%m-%Y %H:%M")),
            "eta": "{}".format(self.eta.strftime("%d-%m-%Y %H:%M")),
            "seats": 7,
            "vehicle": "KCH 001"
        }

        data = json.loads(response.get_data(as_text=True))

        # "/api/v1/rides/rideId"
        ride_id = data['view_ride'].split('/')[4]
        ride_link = "/api/v1/users/rides/"+ride_id

        response = self.client.put(ride_link, data=json.dumps(ride_update),
                                    content_type='application/json')
        self.assert200(response)
        
        response = self.client.get(data['view_ride'], content_type='application/json')

        updated_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(updated_data['seats'], ride_update['seats'])
        
    def test_ride_not_found(self):
       """Test user cannot fetch a non existent ride

       Assert that a GET request to /api/v1/rides/<rideId>
       with a non existent rideId fails with a 404 error.
       """
       response = self.client.get('/api/v1/rides/100', content_type='application/json')

       self.assert404(response)

    def test_making_ride_in_request(self):
        """Test user can request to join a ride

        Assert that a valid POST request to /api/v1/rides/<rideId>/requests
        makes a request to join a ride.
        """

        # create ride
        response = self.create_ride(4)

        data = json.loads(response.get_data(as_text=True))

        ride_request={
            "destination": "Voi"
        }

        response = self.client.post('%s/requests' %data['view_ride'], 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        
        self.assert201(response)

    def test_retract_ride_in_request(self):
        """Test user can retract request to join a ride

        Assert that a valid DELETE request to/api/v1/rides/<rideId>/requests
        removes/retracts a request to join a ride.
        """
         # create ride
        response = self.create_ride(10)

        ride_request={
            "destination": "Voi"
        }

        data = json.loads(response.get_data(as_text=True))

        # make request
        response = self.client.post('%s/requests' %data['view_ride'], 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        self.assert201(response)

        # retract request
        response = self.client.delete('%s/requests' %data['view_ride'], 
                                        content_type='application/json')
        self.assert200(response)
        message = json.loads(response.get_data(as_text=True))['message']
        self.assertEqual(message, "You have retracted request to join ride")

    def test_viewing_requests(self):
        """Test user:driver can view Requests

        Assert that a valid GET request to 
        /users/rides/<rideId>/requests returns requests 
        if you own the ride.
        """
        # create ride
        response = self.create_ride(3)
        self.assert201(response)
        data = json.loads(response.get_data(as_text=True))

        # make ride request
        ride_request={
            "destination": "Voi"
        }
        response = self.client.post('%s/requests' %data['view_ride'], 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        self.assert201(response)

         # "/api/v1/rides/rideId"
        ride_id = data['view_ride'].split('/')[4]
        link = "/api/v1/users/rides/"+ride_id+"/requests"

        # view requests 
        response = self.client.get(link, content_type='application/json')
        
        self.assert200(response)

        # new User
        self.client.post('/api/v1/auth/logout', content_type='application/json')

        self.client.post('/api/v1/auth/register', data=json.dumps(self.ride_pass), 
                            content_type='application/json')

        self.client.post('/api/v1/auth/login', data=json.dumps(self.pass_login), 
                            content_type='application/json')

        response = self.client.get(link, content_type='application/json')                    
        self.assert401(response)

    def test_accept_ride_in_request(self):
        """Test user:driver can accept request to join ride

        Assert that a valid PUT request to 
        /api/v1/users/rides/<rideId>/requests/<number>
        accepts a join request making requester a passenger.
        """

        # create ride 
        response = self.create_ride(4)
        
        ride_link = json.loads(response.get_data(as_text=True))['view_ride']

        # make ride in request
        ride_request={
            "destination": "Voi"
        }

        response = self.client.post('%s/requests' %ride_link, 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        
        request_link = json.loads(response.get_data(as_text=True))['view_request']

        # accept request
        response = self.client.put(request_link, data=json.dumps({'action':'accepted'}), 
                                    content_type='application/json')

        self.assert200(response)
        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual(message, "Ride Request has been 'accepted'")

    def test_reject_ride_in_request(self):
        """Test user:driver can reject a ride request

        Assert that a valid PUT request to /api/v1/rides/<rideId>/requests/<number>
        rejects a ride requests.
        """
        # create ride 
        response = self.create_ride(2)
        
        # make ride in request
        ride_request={
            "destination": "Voi"
        }

        ride_link = json.loads(response.get_data(as_text=True))['view_ride']

        response = self.client.post('%s/requests' %ride_link, 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        
        request_link = json.loads(response.get_data(as_text=True))['view_request']

        # Reject request
        response = self.client.put(request_link, data=json.dumps({'action':"rejected"}),
                        content_type='application/json')

        message = json.loads(response.get_data(as_text=True))['message']

        self.assertEqual(message, "Ride Request has been 'rejected'")


if __name__ == "__main__":
    main(verbosity=2)
