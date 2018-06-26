from unittest import main
import json

from app import create_app
from app.data.ride_data import RIDES, REQUESTS
from . import TestBase

class RideCase(TestBase):
    """Contains tests on a ride and requests made on ride.
    """

    test_ride = {
        "starting_point": "Nairobi-Kencom",
        "destination": "Taita-wunda",
        "depart_time": "26-06-2018 21:00",
        "eta": "27-06-2018 03:00",
        "seats": 4,
        "vehicle": "KCH 001"
    }

    ride_user = {
        "name": "Bob Rider",
        "email": "bobrider@dev.com",
        "password": "12345dfgh"
    }

    rider_login = {
        "email": "bobrider@dev.com",
        "password": "12345dfgh"
    }

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()

        # create User
        self.client.post('/api/v1/auth/register', 
                            data=json.dumps(self.ride_user), 
                            content_type='application/json')
        
        # login user
        self.client.post('/api/v1/auth/login', 
                            data=json.dumps(self.rider_login), 
                            content_type='application/json')
    
    def tearDown(self):
        
        self.client.post('/api/v1/auth/logout', content_type='application/json')
        RIDES.clear()
        REQUESTS.clear()

        self.app = None
        self.client = None

    def test_ride_creation(self):
        """Test creation of a ride offer

        Assert that a valid POST request to /api/v1/rides
        Creates a new ride.    
        """

        response = self.client.post('/api/v1/rides', 
                                        data=json.dumps(self.test_ride), 
                                        content_type='application/json')
        self.assert201(response)
    
    def test_get_available_rides(self):
        """Test Getting all available rides

        Assert that a valid GET request to /api/v1/rides
        returns all available rides
        """


        response = self.client.get('api/v1/rides', content_type='application/json')
        
        self.assert200(response)
    
    def test_get_a_specific_ride(self):
        """Test getting a specific ride

        Assert that a valid GET request to /api/v1/rides/<rideId>
        returns a specific ride
        """

        response = self.client.post('/api/v1/rides', 
                                        data=json.dumps(self.test_ride), 
                                        content_type='application/json')

        self.assert201(response)

        data = json.loads(response.get_data(as_text=True))     
        response = self.client.get(data['view_ride'], content_type='application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(self.test_ride['starting_point'], data['starting_point'])

    def test_ride_details_update(self):
        """Test ride update details

        Assert that a valid PUT request to /api/v1/rides/<rideId>
        updates the ride details.
        """

        response = self.client.post('/api/v1/rides', 
                                        data=json.dumps(self.test_ride), 
                                        content_type='application/json')
                                
        ride_update = {
            "starting_point": "Nairobi-Kencom",
            "destination": "Taita-wunda",
            "depart_time": "26-06-2018 21:00",
            "eta": "27-06-2018 03:00",
            "seats": 7,
            "vehicle": "KCH 001"
        }

        data = json.loads(response.get_data(as_text=True))

        response = self.client.put(data['view_ride'], 
                                    data=json.dumps(ride_update),
                                    content_type='application/json')
        self.assert200(response)
        
        response = self.client.get(data['view_ride'], content_type='application/json')

        updated_data = json.loads(response.get_data(as_text=True))

        self.assertEqual(updated_data['seats'], ride_update['seats'])
        
    def test_ride_not_found(self):
       """Test Ride Not found

       Assert that a GET request to /api/v1/rides/<rideId>
       with a non existent rideId fails with a 404 error.
       """
       response = self.client.get('/api/v1/rides/100', content_type='application/json')

       self.assert404(response)

    def test_making_ride_in_request(self):
        """Test making a request to join a ride

        Assert that a valid POST request to /api/v1/rides/<rideId>/requests
        makes a request to join a ride.
        """

        # create ride
        response = self.client.post('/api/v1/rides', 
                                    data=json.dumps(self.test_ride), 
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))

        ride_request={
            "destination": "Voi"
        }

        response = self.client.post('%s/requests' %data['view_ride'], 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        
        self.assert201(response)

    def test_retract_ride_in_request(self):
        """Test removes a request to join a ride

        Assert that a valid DELETE request to/api/v1/rides/<rideId>/requests
        removes/retracts a request to join a ride.
        """
         # create ride
        response = self.client.post('/api/v1/rides', 
                                    data=json.dumps(self.test_ride), 
                                    content_type='application/json')

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
        self.assert204(response)

    def test_accept_ride_in_request(self):
        """Test accepting a request to join ride

        Assert that a valid POST request to /api/v1/rides/<rideId>/requests/<number>
        accepts a join request making requester a passenger.
        """

        # create ride 
        response = self.client.post('/api/v1/rides', 
                                    data=json.dumps(self.test_ride), 
                                    content_type='application/json')
        
        # make ride in request
        ride_request={
            "userid": "user1",
            "destination": "Voi"
        }

        ride_link = json.loads(response.get_data(as_text=True))['view_ride']

        response = self.client.post('%s/requests' %ride_link, 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        
        request_link = json.loads(response.get_data(as_text=True))['view_request']

        # accept request
        response = self.client.post(request_link, content_type='application/json')

        # get the request
        response = self.client.get(request_link, content_type='application/json')

        request =json.loads(response.get_data(as_text=True))

        self.assertEqual(request['status'], 'accepted')

    def test_reject_ride_in_request(self):
        """Test rejecting a ride request

        Assert that a valid PUT request to /api/v1/rides/<rideId>/requests/<number>
        rejects a ride requests.
        """
        # create ride 
        response = self.client.post('/api/v1/rides', 
                                    data=json.dumps(self.test_ride), 
                                    content_type='application/json')
        
        # make ride in request
        ride_request={
            "userid": "user1",
            "destination": "Voi"
        }

        ride_link = json.loads(response.get_data(as_text=True))['view_ride']

        response = self.client.post('%s/requests' %ride_link, 
                                    data=json.dumps(ride_request), 
                                    content_type='application/json')
        
        request_link = json.loads(response.get_data(as_text=True))['view_request']

        # Reject request
        response = self.client.put(request_link, content_type='application/json')

        # get the request
        response = self.client.get(request_link, content_type='application/json')

        request =json.loads(response.get_data(as_text=True))

        self.assertEqual(request['status'], 'rejected')


if __name__ == "__main__":
    main(verbosity=2)
