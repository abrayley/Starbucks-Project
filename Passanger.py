import numpy as np

class Passanger(object):

    def __init__(self, t, N):

        # time of arrival
        self.arrival_time = t

        #destination floor number
        self.destination_floor = np.random.rand(1,N)

        #time person enters elevator
        self.queue_departure_time = None

        #time person exits elevator
        self.elevator_departure_time = None



