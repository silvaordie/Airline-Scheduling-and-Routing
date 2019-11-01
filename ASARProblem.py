
from search import Problem

class ASARProblem(Problem):
    legs = []
    airports = []
    airplanes = []
    classes = []

    def __init__(self, initial, goal = None):
        pass
    
    def actions(self, state):
        actions = []
        for leg in legs:
            for i in range(len(leg.airplanes)):
                if state.locations[leg.airplanes[i]] == leg.departure:
                    actions.append(Action(leg.airplanes[i], leg.arrival, Time.add( leg.duration , airplanes[leg.airplanes[i]].rotationTime ) , leg.maxProfit - leg4.profit[i])) # é preciso ainda somar a ratation time
        
        return actions
                    
    
    def result(self, state, action):
        new_state=state;
        new_state.location[action.index] = action.departure
        new_state.times[action.index] = Time.add(state.times[action.index] , action.duration)

        return new_state

    
    def goal_test(self, state):
        for l,L in zip(state.locations,state.initialLocations):
            if(l != L):
                return False
        return True
    
    def path_cost(self, c, s1, action, s2):
        return c + action.cost
    
    def heurisitc(state):
        return 0
    
    def load(f):
        for line in f:
            s=line.split()

            if(s[0]== "A"):
                airports.append( Airport(s[1], Time(s[2]), Time(s[3])) )
            elif(s[0] == "C")
                for p in airplanes:
                    if(p.airplaneClass == s[1]):
                        p.setRotTime( Time(s[2]) )

            elif(s[0] == "P")
                airplanes.append( Airplane(s[1], s[2] )
            elif(s[0] == "L")
                avioes = []
                profits =  []
                d = Time(s[3])
                a = next((x for x in airports if x.name == s[1]), None) )
                b = next((x for x in airports if x.name == s[2]), None) ) 

                for k in range(4,len(s)):
                    if((k-4)%2 == 0):
                        for j in range(len(airplanes)):
                            if(airplanes[j].airplaneclass == s[k]):
                                avioes.append(j)
                                profits.append(float(s[k+1]))
                
                legs.append(Leg(a,b,d,avioes,profits))
                    
    def save(f,s):
        pass


class State():   
    initalLocations = []
    
    def _setInitialLocations(locations):
        initalLocations = locations
    
    def __init__(self, times, locations, nrLegs):
        self.times = times
        self.locations = locations
        self.legs = []
        for i in range(nrLegs):
            self.legs.append(1) 
        
class Leg():
    
    def __init__(self, departure, arrival, duration, airplanes, profits):
        self.departure = departure
        self.arrival = arrival
        self.duration = duration
        self.airplanes = airplanes #array de inteiros com o indice do avião no vetor de aviões
        self.profits = profits
        self.maxProfit = max(profits)
        

class Airplane():
    
    def __init__(self, airplaneClass, name, rotTime):
        self.airplaneClass = airplaneClass 
        self.name = name
        self.rotTime = None

    def setRotTime(self, rot):
        self.rotTime=rot

class AirplaneClass():

    def __init__(self, airplaneClass, rotTime) :
        self.name = airplaneClass
        self.rotTime = rotTime

class Airport():
    
    def __init__(self, name, openingTime, closingTime):
        self.name = name
        self.openingTime = openingTime
        self.closingTime = closingTime

class Action():
    
    def __init__(self, index, arrival, duration, cost):
        self.index = index
        self.arrival = arrival
        self.duration = duration
        self.cost = cost

class Time():
    def __init__(self, s)
        self.h = int(s[0:1])
        self.m = int(s[2:3])

    def add(a, b)
        c = Time('0000')
        c.h = a.h + b.h
        c.m = a.m + b.m
        if(c.m > 59):
            c.h = c.h+1
            c.m=c.m-60

        return c

        