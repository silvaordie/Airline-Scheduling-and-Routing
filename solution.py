from copy import deepcopy
from search import Problem

class ASARProblem(Problem):
    
    def __init__(self, initial = None, goal = None):
            self.legs = []
            self.airports = []
            self.airplanes = []
            self.classes = []
            self.nodes = 0
            self.maxProfit= 0
    #Returns all feasible actions given the current state
    def actions(self, state):
        actions = []
        test=[]
        k=0
        nr_null = 0
        
        #Searches all the problem's legs + Initial state legs
        for leg in self.legs:
            #If it is a problem leg
            if(k<len(state.legs) and state.legs[k] == 1):
                #Searches all the available planes
                for i in range(0,len(leg.airplanes)):
                    arrival = leg.duration + state.times[leg.airplanes[i]]
                    duration = leg.duration
                    departure = state.times[leg.airplanes[i]]
                    #If the plane arrives when the airport is closed, delays the departure
                    if leg.arrival.openingTime > arrival:
                        arrival = leg.arrival.openingTime
                        duration = leg.arrival.openingTime - departure
                        departure = leg.arrival.openingTime - leg.duration
                    #If the plane is at the leg's airport, departs while it is still open and arrives while the other airport is open, create an action to return
                    if ((state.locations[leg.airplanes[i]].name == leg.departure.name)  and (leg.arrival.closingTime > arrival) and leg.departure.closingTime > departure):
                        actions.append(Action(leg.airplanes[i], leg.arrival, ( duration + self.airplanes[leg.airplanes[i]].rotTime)  , 1+leg.maxProfit-leg.profits[i]+(1/(leg.maxProfit-leg.minProfit)), k, leg.profits[i], departure))
                        #actions.append(Action(leg.airplanes[i], leg.arrival, ( duration + self.airplanes[leg.airplanes[i]].rotTime)  , 1/leg.profits[i], k, leg.profits[i], departure))
            #If the leg is an initial state leg
            if(leg.departure.name == "NULL"):
                #Searches all the problems airplanes
                for i in range(0,len(leg.airplanes)):
                    #If the plane has no initial airport create an action to return 
                    if (state.locations[leg.airplanes[i]].name == leg.departure.name ):
                        #actions.append(Action(leg.airplanes[i], leg.arrival, leg.arrival.openingTime , 2, k, 0, None))
                        actions.append(Action(leg.airplanes[i], leg.arrival, leg.arrival.openingTime , 2, k, 0, None))
            k=k+1

        #Returns all the available actions
        return actions
        
    #Returns the resulting state of aplying the given action to the current state            
    def result(self, state, action):
        #Copies the current state
        new_state=deepcopy(state)
        #Changes the airplane's location
        new_state.locations[action.index] = action.arrival
        #Shifts the time to the airplane's arrival
        new_state.times[action.index] = (state.times[action.index] + action.duration)
        #If it is a problem's leg, marks it as done and accumulates the profit
        if(action.profit != 0):
            new_state.legs[action.leg] = 0;
            new_state.profit = new_state.profit + action.profit
        else:
            #Sets the airplane's initial airport
            new_state.initialLocations[action.index] = action.arrival
        
        #Adds the current airport to the airplane's path and timeline
        if(state.locations[action.index].name != "NULL"):
            new_state.solution[action.index] = new_state.solution[action.index] + action.departure.toString() + " " + state.locations[action.index].name + " " + new_state.locations[action.index].name + " " 

        self.nodes +=1
        return new_state 

    
    def goal_test(self, state):
        #If all the plane's are at their initial airport, then the first goal condition is valid
        for l in range(len(state.locations)):
            #for L in state.initialLocations:
            if(state.initialLocations[l] == None):
               return False
            if(state.locations[l].name != state.initialLocations[l].name):
                return False
        #If there are no more legs available to be made, then the state is a goal state      
        for l in state.legs:
            if(l==1):
                return False
                
        return True
    
    def path_cost(self, c, s1, action, s2):
        return action.cost
        #return c + action.cost
    
    def heuristic(self, state):
        #return (self.maxProfit - state.state.profit)/self.maxProfit
        #return (self.maxProfit - state.state.profit)
        total = 0
        count=0
        for i in range(len(state.state.legs)):
            if state.state.legs[i]:
                count+=1
                total += 1+(1/(self.legs[i].maxProfit-self.legs[i].minProfit))
                count+=1
        if(count !=0):
            return total/count
        else:
            return 0
      
    #Loads the problem written in file f 
    def load(self, f):
        self.legs = []
        self.airports = []
        self.airplanes = []
        self.classes = []
        A = []
        C = []
        P = []
        L = []
        
        #Reads all the file lines
        for line in f:
            #Saves the file info to be processed in ordder
            s=line.split(" ")
            if(s[0]== "A"):
                A.append(s)
            elif(s[0] == "C"):
                C.append(s)
            elif(s[0] == "P"):
                P.append(s)
            elif(s[0] == "L"):
                L.append(s)
        #Airports        
        for s in A:
            self.airports.append( Airport(s[1], Time(s[2]), Time(s[3])) )
        #Airplanes
        for s in P:
            self.airplanes.append(Airplane(s[2][0:-1], s[1]))
        #Legs
        for s in L:
            avioes = []
            profits = []
            d = Time(s[3])
            a = next((x for x in self.airports if x.name == s[1]), None) 
            b = next((x for x in self.airports if x.name == s[2]), None)  

            for k in range(4,len(s)):
                if((k-4)%2 == 0):
                    for j in range(0,len(self.airplanes)):
                        if(self.airplanes[j].airplaneClass == s[k]):
                            avioes.append(j)
                            profits.append(int(s[k+1]))
            
            self.legs.append(Leg(a,b,d,avioes,profits))
            self.maxProfit = (self.maxProfit + max(profits))
        #Airplane classes
        for s in C:
            for p in self.airplanes:
                if(p.airplaneClass == s[1]):
                    p.setRotTime( Time(s[2]) )
        
        vtimes = []
        vairports = []
        #Creates a ficticial airport for each plane
        for k in range(0,len(self.airplanes)):
            vtimes.append(Time("0000"))
            vairports.append(Airport("NULL", vtimes[0], vtimes[0]))
        #Creates a ficticial leg, from a ficticial airport to a real airport
        for k in range(0, len(self.airports)):
            self.legs.append(Leg(vairports[0],self.airports[k], self.airports[k].openingTime, range(0,len(self.airplanes)), [0] * len(self.airplanes)))
        #Sets the initial state as all planes in ficticial airports
        self.initial = State(vtimes,vairports, len(self.legs)-len(self.airports), self.airplanes)

    #Saves the solution, if found, to a file               
    def save(self, f,state):
        if(state!=None):
            k=0;
            for a in state.solution:
                s = a.split(" ")
                if(len(s)>3):
                    f.write(a+ "\n")
                k+=1
            f.write("P " + str(state.profit))
        print("Nodes",str(self.nodes))

#Class that represents a state of the problem
class State():   

    def __init__(self, times, locations, nrLegs, planes):
        #Initial airplane Airports (assigned in run time) [Array of Airports]
        self.initialLocations = [None] * len(planes)
        #Location of each plane in it's timeline [Array of Times]
        self.times = times
        #Fisical location of each Airplane [Array of Airports]
        self.locations = locations
        #Available legs to perform [Array of 0 or 1]
        self.legs = []
        #Each airplane's landed airport and time of departure [Array of strings]
        self.solution = []
        #State cumulative profit
        self.profit=0
        
        #Initalizes the solutions
        for i in range(len(planes)):
            self.solution.append("S " + planes[i].name + " ")
        #Initialzes the legs
        for i in range(nrLegs):
            self.legs.append(1) 
      
    def __lt__(self, node):
      return (self.profit<node.profit)
      
#Class that represents a problem's Leg    
class Leg():
    
    def __init__(self, departure, arrival, duration, airplanes, profits):
        #Sets the leg's departure Airport
        self.departure = departure
        #Sets the leg's Arrival Airport
        self.arrival = arrival
        #Sets the duration leg's duration as a Time Object
        self.duration = duration
        #Sets the indexes of the possible traveling airplane in the state's vectors [Array of integers]
        self.airplanes = airplanes
        #Sets the profit of each plane in self.airplanes [Array of floats]
        self.profits = profits
        self.maxProfit = max(profits)
        self.minProfit = min(profits)
        if self.maxProfit == self.minProfit:
            self.maxProfit = self.minProfit + 1.1
        
#Class that represents a problem's Airplane
class Airplane():
    
    def __init__(self, airplaneClass, name):
        #Sets the Airplane class as a AirplaneClass object
        self.airplaneClass = airplaneClass 
        #Sets the Airplane name as a String
        self.name = name
        #Airplane rotation time (assigned leter in runtime)
        self.rotTime = None

    #Sets the plane rotation time
    def setRotTime(self, rot):
        self.rotTime=rot

#Class that represents an Airplane Class
class AirplaneClass():

    def __init__(self, airplaneClass, rotTime) :
        #Sets the name of the class as a String
        self.name = airplaneClass
        #Sets the class rotation time as Time Objectt
        self.rotTime = rotTime
        
#Class that represents a problem's Airport
class Airport():
    
    def __init__(self, name, openingTime, closingTime):
        #Sets the airport name
        self.name = name
        #Sets the opening time as a Time object
        self.openingTime = openingTime
        #Sets the clsoing time as a Time Object
        self.closingTime = closingTime
        
#Class that represents a problem's action
class Action():
    
    def __init__(self, index, arrival, duration, cost, leg, profit, departure):
        #Index of the traveling plane in the state's airplanes vector (plane that is flying to a new location)
        self.index = index
        #Airport the plane is flying to as an Airport Object
        self.arrival = arrival
        #Duration of the flight as a Time Object
        self.duration = duration
        #Action's cost as a float
        self.cost = cost
        #Index of the corresponding leg in the State's leg vector
        self.leg = leg
        #Profit of the corresponding plane that is executing the leg
        self.profit = profit
        #Airport from which the plane is leaving as an Airport Object
        self.departure = departure

#Class that represents time instants     
class Time():
    def __init__(self, s):
        #Sets the hour as a string
        self.h = s[0:2]  
        #Sets the minutes as a string
        self.m = s[2:4] 
    
    #Method that sums two time objects
    def __add__(a, b):
        c = Time('0000')
        c.setH( int(a.h) + int(b.h))
        c.setM( int(a.m) + int(b.m))
        
        if(int(c.m) > 59):
            c.setH( int(c.h)+1)
            c.setM( int(c.m)-60)
        
        return c
    
    #Method that finds the time diference between two instants
    def __sub__(a,b):
        c = Time('0000')
        d = (int(a.h) - int(b.h))
        e = (int(a.m) - int(b.m))
        
        if(e<0):
            c.setH(d-1)
            c.setM(e+60)
        else:
            c.setH(d)
            c.setM(e)

        return c
    
    #Changes an object's hour
    def setH(self, h):
        a= str(h)
        if(h<10):
            a = "0" + str(h)
            
        self.h = a
    #Changes an object's minutes
    def setM(self, m):
        a=str(m)    
        if(m<10):
            a = "0" + str(m)

        self.m = a
    
    #Method that compares two time instances, returns true if first is later or equal to the other 
    def __gt__(a, b):
        if (int(a.h) > int(b.h)):
            return True
        elif( (int(a.h) == int(b.h)) and (int(a.m) >= int(b.m))):
            return True
        else:
            return False
    
    #Method that converts the time object to a string with format HHMM
    def toString(self):
        return self.h + self.m
