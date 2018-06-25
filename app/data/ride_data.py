"""Define Ride Data container and Data fetching methods
"""
from app.models import Ride

RIDES = {}

def create_ride(**kwargs):
    """Create a new ride
    """

    ride = Ride(starting_point=kwargs['starting_point'],
            destination=kwargs['destination'],
            depart_time=kwargs['depart_time'],
            eta=kwargs['eta'],
            vehicle=kwargs['vehicle'],
            seats=kwargs['seats'],
            driver=kwargs['driver'])
    
    ride_id = "user{}".format(len(RIDES)+1)

    RIDES[ride_id] = ride.__dict__

    return [ride_id, ride.__dict__]


def get_rides():
    """Get all avalaible ride offers
    """
    return RIDES



