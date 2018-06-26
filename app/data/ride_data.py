"""Define Ride Data container and Data fetching methods
"""
from datetime import datetime, timedelta
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
    
    ride_id = "ride{}".format(len(RIDES)+1)

    RIDES[ride_id] = ride.__dict__

    return [ride_id, ride.__dict__]


def get_rides():
    """Get all avalaible ride offers
    """
    return RIDES


def rides_generator(number):
    """Generate rides
    
    Arguments:
        number {Integer} -- Number of rides you want to create
    """
    
    for x in range(1,number+1):
        current_date = datetime.now()
        depart_time = current_date + timedelta(days=x)
        depart_time = depart_time.strftime("%d-%m-%Y %H:%M")

        eta = current_date + timedelta(days=x+1)
        eta = eta.strftime("%d-%m-%Y %H:%M")

        create_ride(starting_point="town{}-meetingplace{}".format(x,x),
                    destination="town{}".format(x+1),
                    depart_time=depart_time,
                    eta=eta,
                    vehicle="KCH {}{}7b".format(x,x+3),
                    seats=5,
                    driver="user{}".format(x))
        

