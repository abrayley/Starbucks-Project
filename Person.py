import numpy as np

class Person(object):

    timeEnterStbks = None
    mobile = None
    coffee = None

    timeEnterCashQ = None
    timeExitCashQ = None
    timeExitCashSys = None

    timeEnterBarQ = None
    timeExitBarQ = None
    timeExitBarSys = None

    timeExitStbks = None

    abandon = 0
    balk = 0



    # Initialize an Entity
    def __init__(self, start, pMobile, pCoffee, meanPatienceTime,t, probBalkN):

        self.timeEnterStbks = start
        self.mobile = np.random.binomial(1, pMobile)
        self.coffee = np.random.binomial(1, (1 - pMobile) * pCoffee)



        if self.mobile == 0:

            self.patience = np.random.exponential(meanPatienceTime)
            self.abandonTime = t + self.patience

            #do they balk? can only balk if physical queue
            if np.random.rand() <= probBalkN:
                self.balk = 1
        else:
            self.patience = None
            self.abandonTime = None
