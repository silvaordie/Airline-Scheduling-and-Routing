
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
                if state[2*airplanes[i] -1] == leg.departure:
                    actions.append(Action(2*airplanes[i]-1, leg.departure, leg.duration+airplanes[i].rotationTime, leg.maxProfit - leg.profit[i])) # é preciso ainda somar a ratation time
        
        return actions
                    
    
    def result(self, state, action):
        new_state=state;
        new_state.location[action.index] = action.departure
        new_state.times[action.index] = state.times[action.index] + action.duration

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
                airports.append( Airport(s[1], s[2], s[3]) )
            elif(s[0] == "C")
                classes.append( AirplaneClass(s[1], s[2]) )
            elif(s[0] == "P")
                classes.append( Airplane(s[1], next((x for x in classes if x.name == s[2]), None).rotTime ) )
            elif(s[0] == "L")
                avioes = []
                profits =  []
                d = s[3]
                a = next((x for x in airports if x.name == s[1]), None) )
                b = next((x for x in airports if x.name == s[2]), None) ) 

                for k in range(4,len(s)):
                    if((k-4)%3 == 0):
                        durations.append(s[k])
                    if((k-4)%3 == 1):
                        avioes.append(next((x for x in classes if x.name == s[k]), None))
                    if((k-4)%3 == 2):
                        profits.append(float(s[k]))
                    

        
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
    
    def __init__(self, airplaneClass, name):
        self.airplaneClass = airplaneClass
        self.name = name

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
    
    def __init__(self, index, departure, duration, cost):
        self.index = index
        self.departure = departure
        self.duration = duration
        self.cost = cost
        