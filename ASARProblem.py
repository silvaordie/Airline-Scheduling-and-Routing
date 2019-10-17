
from search import Problem

class ASARProblem(Problem):
    legs = []
    
    def __init__(self, initial, goal = None):
        pass
    
    def actions(self, state):
        actions = []
        for leg in legs:
            for i in range(len(leg.airplanes)):
                if state[2*airplanes[i] -1] == leg.departure:
                    actions.append(Action(2*airplanes[i]-1, leg.departure, leg.duration, leg.maxProfit - leg.profit[i]))
        
        return actions
                    
    
    def result(self, state, action):
        pass
    
    def goal_state(self, state):
        pass
    
    def path_cost(self, c, s1, action, s2):
        return c + action.cost
    
    def heurisitc(state):
        pass
    
    def load(f):
        pass
    
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
    
    def __init__(self, rotationTime, airplaneClass, name):
        self.rotationTime = rotationTime
        self.airplaneClass = airplaneClass
        self.name = name
            
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
        