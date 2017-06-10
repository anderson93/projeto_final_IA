'''
    File name: pso_v4.py
    Author: Anderson Henrique de Oliveira Conceicao
    Date created: 29/05/2017
    Date last modified: 02/06/2017
    Python Version: 2.7
'''
from math import sqrt, pow, cos, pi, exp
import random
import numpy as np
from numpy import inf, array
import scipy as sp
 
def run(MaxIt=10000):       #MaxIt - Maximum number of iterations

    #Problem Definition=================================================================================================
    
    def polyRel(bad_lim, good_lim, degree):  #Creates an array with the coefficients of the polynom
        if bad_lim < good_lim:                            
            first_x = bad_lim
            second_x = good_lim
            first_y = abs(1-(bad_lim/good_lim))
            second_y = 0
        elif bad_lim == good_lim:
            first_x = bad_lim*0.5
            second_x = good_lim
            first_y = 1-(first_x/good_lim)
            second_y = 0
            if first_x < 0 or first_x<second_x:
                first_x = good_lim
                second_x = good_lim*1.5
                first_y = 0
                second_y = abs(1-(good_lim/second_x))
        else:
            first_x = good_lim
            second_x = bad_lim
            first_y = 0
            second_y = abs(1-(bad_lim/good_lim))
    
        X = [ 0, first_x, second_x, 1 ]
        Y = [ 1, first_y, second_y, 1 ]
        
        try:
            P = sp.polyfit(X, Y, degree)
        except sp.RankWarning :             #To adjust if the polynom is not well conditioned
            P = sp.polyfit(X, Y, degree-1)
    
        return P

    #It creates the polynom that defines the parameter dynamics
    #                    Bad     Good  Degree
    P0 = list(polyRel( 0.57962, 0.59091, 3))    #AAET    
    P1 = list(polyRel( 0.58664, 0.59591, 3))    #AAST
    P2 = list(polyRel( 0.00292, 0.00021, 3))    #VI
    P3 = list(polyRel( 0.11682, 0.07932, 3))    #QMA
    P4 = list(polyRel( 0.11947, 0.12379, 3))    #IMAI
    P5 = list(polyRel( 0.58417, 0.58726, 3))    #VA
    
    # Polynomial translation         A*X^3    +    B*X^2   +    C*X^1   +    D*X^0 =====================================
    def polyeval(x, poly): return poly[0]*x**3+poly[1]*x**2+poly[2]*x**1+poly[3]*x**0
    
    def fitnessFunc(x):
        AAET = polyeval(x[0], P0)   # AAET =  x[0] ;
        AAST = polyeval(x[1], P1)   # AAST =  x[1] ;
        VI   = polyeval(x[2], P2)   # VI   =  x[2] ; 
        QMA  = polyeval(x[3], P3)   # QMA  =  x[3] ;
        IMAI = polyeval(x[4], P4)   # IMAI =  x[4] ;
        VA   = polyeval(x[5], P5)   # VA   =  x[5].
        #Fitness function
        try: return ((VA/(AAST-AAET))*(VI/(AAST-AAET))**(-1)*(AAST/AAET)**(-1)*(QMA/IMAI)**(-1))
        except ZeroDivisionError: return 'inf'
                                                                        
    nVar = 6                            #Number of dimensions                         
    VarMin = 0                          #Lower bound of decision variables              
    VarMax = 1                          #Upper bound of decision variables             
    MaxVelocity = 0.002*(VarMax-VarMin) #Velocity upper bound            
    MinVelocity = -MaxVelocity          #Velocity lower bound               
    
    #Constriction coefficients==========================================================================================
    kappa = 1
    phi1 = 2.05
    phi2 = 2.05
    phi = phi1 + phi2
    chi = 2*kappa/abs(2-phi-sqrt(phi**2-4*phi))     
    random.seed(0)
    
    #Parameters of PSO==================================================================================================
    range_cost = 1.5         #Defines the range in which the algorithm will adjust around zero cost
    nPop = 35                #Population size (swarm size)
    w = chi                  #Inertia coefficient
    c1 = chi*phi1            #Personal acceleration coefficient
    c2 = chi*phi2            #Social acceleration coefficient
    GlobalBestCost = '-inf'  #Global best cost
    GlobalBestPosition = []  #Global best position
    Swarm = []               #Swarm population array
    
    #Useful functions===================================================================================================

    #Unnormalize the value
    def unnormalize(n,min,max): 
        return (max-min)*n+min  #unnormalize(number, minimum value, maximal value)
    #Creates an array of random numbers
    def randArray(size):        
        aux = []
        for i in xrange(0,size): aux.append(random.uniform(VarMin,VarMax))
        return aux
    #It limits the number in a defined range
    def clamp(x,max,min):             #clamp(array, max bound, min bound);
        if isinstance(x, list):       #or clamp(scalar, max bound, min bound);
            for i in xrange(0, len(x)):
                if x[i] >= max: x[i] = max
                elif x[i] <= min: x[i] = min
        else:
            if x >= max: x = max
            elif x <= min: x = min
        return x
    
    #Class definition===================================================================================================
    class Particle(object):              #Defining the Particle's class
        def __init__(self, Position=None, Velocity=None, \
            Cost=None, BestPosition=None, BestCost=None):

            self.Position =[]            #Characteristics of the particle
            self.Velocity = []
            self.Cost = 0
            self.BestPosition = []
            self.BestCost = []
    
    #Initializing the algorithm=========================================================================================
    #Swarm population array
    for i in xrange(0,nPop): Swarm.append(Particle())
    
    #Initialize population members
    for i in xrange(0,nPop):
        #Generate random solution
        Swarm[i].Position = list(randArray(nVar))       
        #Initialize velocity
        Swarm[i].Velocity = [0]*nVar                    
        #Evaluation
        Swarm[i].Cost = fitnessFunc(Swarm[i].Position) 
        #Update personal best position
        Swarm[i].BestPosition = list(Swarm[i].Position)       
        #Update personal best cost
        Swarm[i].BestCost = Swarm[i].Cost               
        #It compares with the Global Best Cost and updates the value
        if Swarm[i].BestCost < GlobalBestCost:
            GlobalBestCost = Swarm[i].BestCost
            GlobalBestPosition = list(Swarm[i].BestPosition)
    
    #Array to hold best cost value on each iteration
    BestCosts = []
    BestPositions = []
    BestCosts.append(GlobalBestCost)
    BestPositions.append(GlobalBestPosition)
    
    #Main loop of PSO
    for i in xrange(1,MaxIt):
        
        for j in xrange(0,nPop):
            # Update Velocity: v = w*v + c1*rand*(pbest-x) + c2*rand*(gbest-x)
            Swarm[j].Velocity = list(w*np.array(Swarm[j].Velocity) \
                                +c1*random.uniform(0,1)*(np.array(Swarm[j].BestPosition)-np.array(Swarm[j].Position)) \
                                +c2*random.uniform(0,1)*(np.array(GlobalBestPosition)-np.array(Swarm[j].Position)))
            #Applying lower and upper bound limits
            Swarm[j].Velocity = clamp(Swarm[j].Velocity, MaxVelocity, MinVelocity)         
            #Update position
            Swarm[j].Position = np.array(Swarm[j].Position) + np.array(Swarm[j].Velocity)  
            #Applying lower and upper bound limits, by defining 
            #the lower bound limit as: mean - standard deviations
            #and the upper bound limits as: mean + standard deviations
            Swarm[j].Position[0] = clamp(Swarm[j].Position[0], 1, 0.16667)             # x = AAET = x[0] ;
            Swarm[j].Position[1] = clamp(Swarm[j].Position[1], 1, 0.16667)             # y = AAST = x[1] ;
            Swarm[j].Position[2] = clamp(Swarm[j].Position[2], 0.00021+0.00075, 0)     # z =  VI  = x[2] ;
            Swarm[j].Position[3] = clamp(Swarm[j].Position[3], 0.07932+0.12049, 0)     # v = QMA  = x[3] ;
            Swarm[j].Position[4] = clamp(Swarm[j].Position[4], 0.12379+0.12910, 0)     # w = IMAI = x[4] ;
            Swarm[j].Position[5] = clamp(Swarm[j].Position[5], 0.97727, 0)             # u =  VA  = x[5] .
            #Evaluation
            Swarm[j].Cost = fitnessFunc(Swarm[j].Position)
            #Update personal best
            if (Swarm[j].Cost <= Swarm[j].BestCost and Swarm[j].Cost > -range_cost) or\
               (Swarm[j].Cost >= Swarm[j].BestCost and Swarm[j].Cost < range_cost):
                Swarm[j].BestPosition = list(Swarm[j].Position)  
                Swarm[j].BestCost = Swarm[j].Cost
            #Update global best
            if (Swarm[j].BestCost <= GlobalBestCost and Swarm[j].BestCost > -range_cost) or\
               (Swarm[j].BestCost >= GlobalBestCost and Swarm[j].BestCost < range_cost):          
                GlobalBestCost = Swarm[j].BestCost
                GlobalBestPosition = list(Swarm[j].Position)
            #Stores the best cost value
            BestCosts.append(GlobalBestCost)         
            #Stores the best position    
            BestPositions.append(GlobalBestPosition) 

    #Unnormalizing the variables by the limits defined on the table=====================================================
    AAET = unnormalize(BestPositions[-1][0], 0, 4387014266.17000)
    AAST = unnormalize(BestPositions[-1][1], 0, 2561890616.28000)
    VI   = unnormalize(BestPositions[-1][2], 25.18000, 268931997.14000)
    QMA  = unnormalize(BestPositions[-1][3], 1, 63)
    IMAI = unnormalize(BestPositions[-1][4], 0, 1056)
    VA   = unnormalize(BestPositions[-1][5], 0, 39944239.59000)
    
    # x = AAET = x[0] ; y = AAST = x[1] ; z = VI = x[2] ; v = QMA = x[3] ; w = IMAI = x[4] ; u = VA = x[5]==============
    print "The results are ready!"
    print "\n"
    print "This was the Best Cost:", BestCosts[-1]
    print "This was the Best Position:", BestPositions[-1]

    return BestCosts[-1],BestPositions[-1]


