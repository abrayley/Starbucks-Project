import numpy as np
from Person import Person
from System import System
from Employee import Employee


# This class is for modeling the entire starbucks system.
class Starbucks(object):

    def __init__(self):

        # time of events
        self.times = []

        #time customer enters bar queue
        self.timesEnterBar = []

        # number of people in queues at every event time
        self.barqlength = []
        self.cashqlength = []

        # All Customers Who Showed up (including Balking and abandonment)
        self.allCustomers = []

        #The time mobile customers enter the bar queue
        self.mobileCustomersEnterTime = []

        #Customers who did not balk (entered queue)
        self.customersEnterQueue = []

        #customers who didn't balk and didn't abandoned
        self.allCustomersNotBalkNotAbandon= []

        # number of finished customers
        # Customers who have completed service
        self.completedCustomers = []
        self.completedCustomersBar = []
        self.completedCustomersCash = []

        # customers balking
        self.balkingCustomers = []
        self.numBalk = 0

        # Customers who abandoned
        self.abandonedCustomers = []
        self.numAbandon = 0

        # number of people being serviced at each event time

        self.numberOccupiedServersCash = []
        self.numberOccupiedServersBar = []

        self.numberUnoccupiedServersCash= []
        self.numberUnoccupiedServersBar = []

        # number of servers on 'vacation' at every event time

        self.numberServersOnVacationCash = []
        self.numberServersOnVacationBar = []

        #list of employees
        self.unoccupiedServersCash = []
        self.unoccupiedServersBar = []
        self.occupiedServersCash = []
        self.occupiedServersBar = []
        self.vacationServersCash = []
        self.vacationServersBar = []


        # indicator if employee needs to switch
        self.employeeBartoCash = 0
        self.employeeCashToBar = 0

        # is switch switch_possible?
        self.switch_possible_cash_to_bar = 0
        self.switch_possible_bar_to_cash = 0

        # storing data
        self.cashServiceStarts = []  # time when cash service starts
        self.barServiceStarts = []  # time when bar service starts


    def enter_cash(self, customer):
        #add to cash queue
        self.cash.arrive_at_queue(customer)
        customer.timeEnterCashQ = self.t
        # queue length changes check if need switch
        self.check_if_switch_necessary()
        #check if can start service
        self.serve_next_customer_cash()



    def enter_bar(self, customer):
        #update times at which people enter bar
        self.timesEnterBar.append(self.t)

        # add to bar queue
        self.bar.arrive_at_queue(customer)
        customer.timeEnterBarQ = self.t
        #queue length changes check if need switch
        self.check_if_switch_necessary()
        # start service if available server
        self.serve_next_customer_bar()


    def exit_cash(self, customer):
        # update customer
        customer.timeExitCashSys = self.t

        # if person only orders coffee they leave. if they have complex order they go to bar
        if customer.coffee == 0:
            # person arrives to the bar queue
            self.enter_bar(customer)

        else:
            # person leaves
            customer.timeExitStbks = self.t
            self.completedCustomers.append(customer)

        # Server becomes available
        s = self.occupiedServersCash[0]
        self.unoccupiedServersCash.append(s)
        self.occupiedServersCash.pop(0)

        #server becomes available- check if can switch:
        if self.employeeBartoCash ==1 or self.employeeCashToBar ==1:
            self.perform_server_switch()

        #start service if available.
        self.serve_next_customer_bar()
        self.serve_next_customer_cash()



        #check if system empty
        self.server_leave_vacation()

    def exit_bar(self, customer):
        # update customer
        customer.timeExitBarSys = self.t
        customer.timeExitStbks = self.t
        self.completedCustomers.append(customer)
        # Server becomes available
        s = self.occupiedServersBar[0]
        self.unoccupiedServersBar.append(s)
        self.occupiedServersBar.pop(0)

        #server becomes available- check if can switch:
        if self.employeeBartoCash ==1 or self.employeeCashToBar ==1:
            self.perform_server_switch()

        #start service if available.
        self.serve_next_customer_bar()
        self.serve_next_customer_cash()

        #check if system empty
        self.server_leave_vacation()

    def serve_next_customer_bar(self):
        if len(self.bar.waitingCustomers) > 0 and len(self.unoccupiedServersBar) > 0:
            # get next person in line
            customer = self.bar.waitingCustomers[0]
            customer.timeExitBarQ = self.t
            #the server who will become occupied
            s = self.unoccupiedServersBar[0]
            self.occupiedServersBar.append(s)
            self.unoccupiedServersBar.pop(0)

            self.bar.start_service()
            self.barServiceStarts.append(self.t)

            # queuelength changes: check if need switches
            self.check_if_switch_necessary()


    def serve_next_customer_cash(self):
        if len(self.cash.waitingCustomers) > 0 and len(self.unoccupiedServersCash) >0:
            # find next customer in line
            customer = self.cash.waitingCustomers[0]
            customer.timeExitCashQ = self.t


            #the server who will become occupied
            s = self.unoccupiedServersCash[0]
            self.occupiedServersCash.append(s)
            self.unoccupiedServersCash.pop(0)

            self.cash.start_service()
            self.cashServiceStarts.append(self.t)

            # queuelength changes: check if need switches
            self.check_if_switch_necessary()

    def check_if_switch_necessary(self):

        if not self.isSwitchingSystem:
            self.employeeCashToBar = 0
            self.employeeBartoCash = 0
            return None

        # perform this when queue length changes
        if len(self.barqlength) > 0 and len(self.cashqlength) >0:

            if self.barqlength[-1] >0 and self.cashqlength[-1]>0:
                ratio = self.cashqlength[-1]/self.barqlength[-1]

                if ratio < self.switchRatioCashtoBar:
                    self.employeeCashToBar = 1

                if ratio > self.switchRatioBartoCash and (len(self.occupiedServersCash)+ len(self.unoccupiedServersCash))<self.numCashReg:
                    self.employeeBartoCash = 1

            elif self.cashqlength[-1] == 0 and self.barqlength[-1] > 2:
                #If no one in cash queue and more than 2 people in bar queue
                #move from cash to bar
                self.employeeCashToBar = 1

            elif self.cashqlength[-1]> 0  and self.barqlength[-1] == 0 and (len(self.occupiedServersCash)+ len(self.unoccupiedServersCash))<self.numCashReg:
                self.employeeBartoCash = 1
        #return(max(self.employeeBartoCash, self.employeeCashToBar))
        # check if can perform switch
            if self.employeeBartoCash ==1 or self.employeeCashToBar ==1:
                self.perform_server_switch()





    def perform_server_switch(self):

        # don't do any switching if both booleans are 0.
        if self.employeeBartoCash == 0 and self.employeeCashToBar == 0:
            return None

        # switch Bar to Cash
        if self.employeeBartoCash ==1 and len(self.unoccupiedServersBar) >=1:
            #reset
            self.employeeBartoCash =0
            self.switch_possible_bar_to_cash = 0

            s = self.unoccupiedServersBar[0]
            #switch employee's location
            s.switchLocation()
            #remove from unoccupied Bar server list
            self.unoccupiedServersBar.pop(0)
            # add to unoccupied Cash list
            self.unoccupiedServersCash.append(s)

            self.serve_next_customer_cash()

        #switch cash to bar
        if self.employeeCashToBar ==1 and len(self.unoccupiedServersCash) >=1:
            #reset
            self.employeeCashToBar = 0
            self.switch_possible_cash_to_bar = 0

            s = self.unoccupiedServersCash[0]
            #switch employee's location
            s.switchLocation()
            #remove from unoccupied Bar server list
            self.unoccupiedServersCash.pop(0)
            # add to unoccupied Cash list
            self.unoccupiedServersBar.append(s)

            self.serve_next_customer_bar()


    def server_leave_vacation(self):
        #requirements: system must be empty, there must be unoccupied server and no other servers from in stbks on vacation
        if self.vacationMeanLength == 0:
            return None

        if self.cash.inSystem == 0 and len(self.unoccupiedServersCash)>0 and (len(self.vacationServersCash)+ len(self.vacationServersBar)) ==0:

            empl = self.unoccupiedServersCash[0]
            empl.vacation = 1
            self.vacationServersCash.append(empl)

            self.unoccupiedServersCash.pop(0)


        if self.bar.inSystem == 0 and len(self.unoccupiedServersBar)>0 and (len(self.vacationServersCash)+len(self.vacationServersBar)) ==0:

            empl = self.unoccupiedServersBar[0]
            empl.vacation = 1
            self.vacationServersBar.append(empl)

            self.unoccupiedServersBar.pop(0)

    def server_return_vacation(self,empl):

        empl.vacation = 0
        if empl.location ==0:
            self.vacationServersCash.pop(0)
        else:
            self.vacationServersBar.pop(0)

        #check where the employee goes
        if  empl.location == 0 and len(self.occupiedServersCash) < self.numCashReg:
            #go to cash
            empl.location = 0
            self.unoccupiedServersCash.append(empl)
            #check if can serve someone
            self.serve_next_customer_cash()

        else:
            #go to bar
            empl.location = 1
            self.unoccupiedServersBar.append(empl)
            #check if can serve someone
            self.serve_next_customer_bar()

    def abandon_cash_queue(self, customer):
        #update customer
        customer.abandon = 1
        customer.timeExitStbks = customer.abandonTime
        customer.timeExitCashQ = customer.abandonTime

        self.numAbandon += 1
        self.abandonedCustomers.append(customer)

    def simulation(self, starbucksArrivalRate = 100, pMobile = 0.7,
                   pCoffee = 0.4, cashRate = 40, barRate = 17,
                   simDuration = 10, cTotal = 4, initialCashC = 1, numCashReg = 2,switchRatioCashtoBar = 0.5,
                   switchRatioBartoCash = 1, meanPatienceTime = 10, vacationMeanLength = 2, isSwitchingSystem = True, isBalkingSystem = True):
        '''
        StarbucksArrivalRate = total arrivals to starbucks per hour
        pMobile = percent of arrivals that are mobile
        pCoffee = percent of people at cash who only order coffee (served at cash)
        CashRate = service rate at cash (ppl/hr)
        BarRate = service rate at Bar (pp/hr)
        simDuration = how long to run the simulation
        cTotal = total number of servers in Stbks.
        initialCashC = Inital number of cash servers
        cCash= total number of cash servers
        cBar = servers at bar
        vacationMeanLength = how long servers take vacation
        numCashReg = number of cash registers there are. can not have more cash servers than numCashReg
        switchRatioCashtoBar = cashQlen/barQlen at which employee switches from cash to bar
        switchRatioBartoCash = cashQlen/barQlen at which employee switches from bar to cash
        isSwitchingSystem = boolean to deterine if cashiers and baristas switch
        '''

        self.starbucksArrivalRate = starbucksArrivalRate
        self.cTotal = cTotal
        self.pMobile = pMobile
        self.pCoffee = pCoffee
        self.cashRate = cashRate
        self.barRate = barRate
        self.simDuration = simDuration
        self.cCash = min(initialCashC,numCashReg)
        self.cBar = self.cTotal - self.cCash
        self.switchRatioCashtoBar = switchRatioCashtoBar
        self.switchRatioBartoCash = switchRatioBartoCash
        self.numCashReg = numCashReg
        self.vacationMeanLength = vacationMeanLength
        self.isSwitchingSystem = isSwitchingSystem
        self.isBalkingSystem = isBalkingSystem


        # Two systems/ queues (cash and Bar)

        cash = System( waiting = [])
        bar = System( waiting = [])
        self.cash = cash
        self.bar = bar

        #initialize  servers
        locations = [0]*int(self.cCash) + [1]* int(self.cBar)
        self.servers =  np.array([Employee(locations[i]) for i in range(cTotal)])

        for server in self.servers:
            if server.location ==0:
                self.unoccupiedServersCash.append(server)
            else:
                self.unoccupiedServersBar.append(server)

        #simulation conditions
        self.t= 0
        t_end = simDuration


        rateTotal = self.starbucksArrivalRate + cashRate * len(self.occupiedServersCash)+ barRate * len(self.occupiedServersBar)
        nextEventTime = self.t+ np.random.exponential(1 / rateTotal)

        # run simulation as long as we are less than the simulation duration
        while self.t< t_end:
            # ABANDONMENT
            # check if there is any abandonment between t and next event time:
            for ppl in self.cash.waitingCustomers:

                if ppl.abandonTime < nextEventTime:
                    self.abandon_cash_queue(ppl)
                    self.cash.waitingCustomers.remove(ppl)

            #check if servers switch
            self.check_if_switch_necessary()

            # we are now at the next event
            self.t= nextEventTime

            '''
            determine what the next event is. There are three options:
            0 = person arrives to system
            1 = service at cash finishes
            2 = service at bar finishes
            3 = server returns from vacation
            '''

            u = np.random.rand()

            if u <= self.starbucksArrivalRate / rateTotal:
                # this is an event 0 = person arrives
                event = 0
            elif (u <= (self.starbucksArrivalRate+ cashRate * len(self.occupiedServersCash)) / rateTotal) and len(self.occupiedServersCash) >0:
                event = 1  # cash finish
            elif (u <=  self.starbucksArrivalRate + cashRate * len(self.occupiedServersCash)+ barRate * len(self.occupiedServersBar))/ rateTotal and len(self.occupiedServersBar) >0:
                event = 2 # bar finish
            else:
                if len(self.vacationServersBar) >0 or len(self.vacationServersCash) >0  :
                    event = 3  # vacation finish
                else:
                    print('Event assignment Error')
            #print('event:')
            #print(event)
            #print(u)
            #print((60/self.vacationMeanLength)*(len(self.vacationServersBar)+len(self.vacationServersBar))/rateTotal)


            # person arrives
            if event == 0:
                '''
                Person arrives.
                Determine if cashier / barista should switch / switch back:
                '''

                # create customer

                #determine the probability of balking

                if len(self.cashqlength) >=1 and self.isBalkingSystem:
                    probBalkN = min(self.cashqlength[-1]/25,1)
                else:
                    probBalkN = 0

                #probBalkN = 0.5
                #probBalkN = 0


                customer = Person(self.t, pMobile, pCoffee, meanPatienceTime, self.t, probBalkN)

                # add customer to total list of customers who enter stbks (mobile and physical)
                self.allCustomers.append(customer)

                if customer.balk == 0:

                    #add person to list of people who entered
                    self.customersEnterQueue.append(customer) # physical or mobile

                    # if customer.mobile = 0 they are a pysical customer and go to the cash first
                    if customer.mobile == 0:

                        self.enter_cash(customer)

                    else:  # go to bar
                        self.mobileCustomersEnterTime.append(self.t)
                        self.enter_bar(customer)
                else:
                    self.balkingCustomers.append(customer)
                    self.numBalk += 1

            elif event == 1:

                '''
                Cash service ends
                If there is someone in the queue start service immediately.

                '''
                # get and update the customer who is leaving
                customer = self.cash.end_service()

                self.exit_cash(customer)

                self.completedCustomersCash.append(customer)



            elif event == 2:

                '''
                Bar service ends
                If there is someone in the bar queue start service immediately.

                '''
                # get the customer who is leaving
                customer = self.bar.end_service()

                self.exit_bar(customer)

                # add customer to list of customers who have completed bar service
                self.completedCustomersBar.append(customer)
                #self.completedCustomers.append(customer)

            else:
                #print('returns from vacation')
                if len(self.vacationServersBar) >0:
                    empl = self.vacationServersBar[0]
                else:
                    empl = self.vacationServersCash[0]

                self.server_return_vacation(empl)



            # calc time for next event

            if self.vacationMeanLength == 0:
                vacationMeanRate = 0
            else:
                vacationMeanRate = (60/self.vacationMeanLength)

            rateTotal = self.starbucksArrivalRate + cashRate * len(self.occupiedServersCash)+ barRate * len(self.occupiedServersBar) + vacationMeanRate*(len(self.vacationServersBar)+len(self.vacationServersCash))

            #print((len(self.vacationServersBar)))
            #print((len(self.vacationServersCash)))
            #print((60/self.vacationMeanLength)*(len(self.vacationServersCash)+len(self.vacationServersBar)))

            nextEventTime = self.t+ np.random.exponential(1 / rateTotal)

            # update and store values
            self.times.append(self.t)
            self.cashqlength.append(np.size(self.cash.waitingCustomers))
            self.barqlength.append(np.size(self.bar.waitingCustomers))
            self.numberOccupiedServersCash.append(len(self.occupiedServersCash))
            self.numberOccupiedServersBar.append(len(self.occupiedServersBar))
            self.numberUnoccupiedServersCash.append(len(self.unoccupiedServersCash))
            self.numberUnoccupiedServersBar.append(len(self.unoccupiedServersBar))
            self.numberServersOnVacationCash.append(len(self.vacationServersCash))
            self.numberServersOnVacationBar.append(len(self.vacationServersBar))


        for i in range(0,len(self.customersEnterQueue)):
            if self.customersEnterQueue[i].abandon ==0:
                self.allCustomersNotBalkNotAbandon.append(self.customersEnterQueue[i])
