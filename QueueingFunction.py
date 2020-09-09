
# coding: utf-8

# In[3]:


#Input
#q_type: Type of queue, takes value 'MG1', 'MMc', 'MGc', 'MMcN'
#Lambda:  arrival rate
#Mu:  service rate
#c: # of servers
#N:  #capacity of system including those in service

#Output
#rho:  lambda/mu
#L:  average number of people in system
#w:  average time in system
#wQ:  average time waiting in queue
#LQ:  average number of people in queue
#P0:  probability of system being empty


def Queueing(q_type, Lambda, Mu, C, Sigma2 = 1, N = 100000, K = 1000):
    '''
    #Input
    #q_type: Type of queue, takes value 'MG1', 'MMc', 'MGc', 'MMcN'
    #Lambda:  arrival rate
    #Mu:  service rate
    #c: # of servers
    #N:  #capacity of system including those in service

    #Output
    #rho:  lambda/mu
    #L:  average number of people in system
    #w:  average time in system
    #wQ:  average time waiting in queue
    #LQ:  average number of people in queue
    #P0:  probability of system being empty
    '''
  
    import numpy as np
    
    if q_type == 'MG1':
        if Lambda > Mu:
            print('The arrival rate must be less than the service rate')
            return None
        elif Lambda <= 0 or Mu <= 0:
            print('Arrival and Service parameters must be positive')
            return None
        elif Sigma2 < 0:
            print('Variance must be nonnegative')
            return None
        rho = (Lambda + 0.0)/Mu
        L = (rho + rho**2 * (1.0 + Sigma2*Mu**2))/(2*(1-rho))
        w = L/Lambda
        wQ = w - 1.0/Mu
        LQ = wQ*Lambda
        P0 = 1 - rho
        
        outputs = (rho, L, w, wQ, LQ, P0)
        return outputs
    elif q_type == 'MMc':
        Sigma2 = Mu 
        if Lambda > C*Mu:
            print('The arrival rate must be less than the service rate')
            return None
        elif Lambda <= 0 or Mu <= 0:
            print('Arrival and Service parameters must be positive')
            return None
        elif C < 0 or C/1.0 != C:
            print('C must be a positive integer')
            return None
        rho = (Lambda + 0.0)/(C*Mu)
        OfferedLoad = Lambda/Mu
        Factor = 1
        P0 = 1
        for i in range(1,C):
            Factor = Factor*OfferedLoad/(i+0.0)
            P0 = P0 + Factor
        P0 = P0 + Factor*OfferedLoad/(C*(1-rho)*1.0)
        P0 = 1.0/P0
        
        L = OfferedLoad + (OfferedLoad**(C+1)*P0)/(C*np.math.factorial(C)*(1-rho)**2)
        w = L/Lambda
        wQ = w - 1.0/Mu
        LQ = wQ*Lambda
        P0 = P0
        outputs = (rho, L, w, wQ, LQ, P0)
        return outputs
    elif q_type == 'MGc':
        if Lambda > C*Mu:
            print('The arrival rate must be less than the service rate')
            return None
        elif Lambda <= 0 or Mu <= 0:
            print('Arrival and Service parameters must be positive')
            return None
        elif Sigma2 < 0:
            print('Variance must be nonnegative')
            return None
        elif C < 0 or C/1.0 != C:
            print('C must be a positive integer')
            return None
        
        rho = (Lambda + 0.0)/(C*Mu)
        OfferedLoad = Lambda/Mu
        Factor = 1
        P0 = 1
        for i in range(1,C):
            Factor = Factor*OfferedLoad/(i+0.0)
            P0 = P0 + Factor
        P0 = P0 + Factor*OfferedLoad/(C*(1-rho)*1.0)
        P0 = 1.0/P0
        
        LQ = OfferedLoad + ((1+cv2)/2.0)*(OfferedLoad**(C+1)*P0)/(C*np.math.factorial(C)*(1-rho)**2)
        wQ = LQ/Lambda
        w = wQ + 1.0/Mu
        L = w*Lamda
        P0 = P0
        outputs = (rho, L, w, wQ, LQ, P0)
        return outputs
    elif q_type == 'MMcN':
        if Lambda >= C*Mu:
            print('The arrival rate must be less than the service rate')
            return None
        elif Lambda <= 0 or Mu <= 0:
            print('Arrival and Service parameters must be positive')
            return None
        elif Sigma2 < 0:
            print('Variance must be nonnegative')
            return None
        elif C < 0 or C/1.0 != C:
            print('C must be a positive integer')
            return None
        elif N < C:
            print('N must be at least as large as C')
            return None
        rho = (Lambda + 0.0)/(C*Mu)
        OfferedLoad = Lambda/Mu
        Factor = 1
        P0 = 1
        for i in range(1,C):
            Factor = Factor*OfferedLoad/(i+0.0)
            P0 = P0 + Factor
        if C > N:
            rhosum = rho
            if C > N + 1:
                for i in range(C+2,N+1):
                    rhosum += rho**(i-C)
            P0 += Factor * rhosum
        P0 = 1.0/P0
        PN = OfferedLoad**N /(np.math.factorial(C)*C**(N-C))*P0
        LQ = P0*OfferedLoad**C*rho/(np.math.factorial(C)*(1-rho)**2 * (1 - rho**(N-C) -(N-C)*rho**(N-C)*(1-rho)))
        LambdaEffective = Lambda*(1-PN)
        wQ = LQ/LambdaEffective
        w = wQ + 1.0/Mu
        L = w*LamdaEffective
        outputs = (rho, L, w, wQ, LQ, P0, PN, LambdaEffective)
        return outputs
    else:
        print('Please choose a supported type of queue')
        return None
            
            
            
    
    
    


# In[4]:


