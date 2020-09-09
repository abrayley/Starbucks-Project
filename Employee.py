import numpy as np
class Employee(object):

    def __init__(self,location):

        #locatio Cash =0 , bar = 1
        self.location = location
        self.busy = 0
        self.vacation = 0
    def occupied(self):
        self.busy = 1
    def unoccupied(self):
        self.busy = 0


    def switchLocation(self):
        if self.location ==0:
            self.location = 1
        else:
            self.location = 0
