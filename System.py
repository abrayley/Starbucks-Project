class System(object):
    ''' system is the class for the different processes. This includes the cash and the bar.'''


    # list of customers waiting for service.
    waitingCustomers = []

    # Initialize the system (cash/bar)
    def __init__(self, waiting):
        '''
        c = number of servers
        cBusy = number of busy servers
        waiting = list of waiting customers
        inService = list of customers being served  (being served - NOT INCL.QUEUE)
        serviceRate = rate of service per server
        '''

        #self.c = c
        #self.cBusy = cBusy

        self.inService = [] # number of people
        self.waitingCustomers = waiting
        self.inSystem = len(self.inService) + len(self.waitingCustomers)

    # new customer arrives to the system.
    def arrive_at_queue(self, newcustomer):
        # new arrival is a customer which is an person class
        self.waitingCustomers.append(newcustomer)

        self.inSystem = len(self.inService) + len(self.waitingCustomers)
    # start service. Move from waiting to getting service
    def start_service(self):
        #self.cBusy += 1

        # take the first cusomter in the waiting customer list
        customerLeavingQueue = self.waitingCustomers[0]

        # add the new customer to the 'inSystem'
        self.inService.append(customerLeavingQueue)

        # update waiting people
        self.waitingCustomers.pop(0)

        self.inSystem = len(self.inService) + len(self.waitingCustomers)

    def end_service(self):
        # one server becomes available
        #self.cBusy -= 1

        # update who's in system (the person top of the list leaves)
        leavingCustomer = self.inService[0]

        # remove the first person from the list of people in the system
        self.inService.pop(0)

        self.inSystem = len(self.inService) + len(self.waitingCustomers)

        return leavingCustomer
