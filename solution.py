from copy import deepcopy
from search import Problem
#c :maxProfit-(leg.maxProfit-leg.minProfit)
#h: leg.maxProfit-airplane.profit

class ASARProblem(Problem):

    def __init__(self, initial = None, goal = None):
            self.legs = []
            self.airports = []
            self.airplanes = []
            self.classes = []
            self.maxProfit= 0

    def actions(self, state):
        actions = []
        test=[]
        k=0
        nr_null = 0
        
        for i in range(0,len(self.airplanes)):
            if state.locations[i].name == 'NULL':
                nr_null += 1
            #test.append(self.airplanes[i].name + ' ' + state.locations[i].name + " " + state.times[i].toString())
        #print(test)
        
        
        for leg in self.legs:
            if(k<=len(state.legs) and state.legs[k] == 1):
                for i in range(0,len(leg.airplanes)):
                    arrival = leg.duration + state.times[leg.airplanes[i]]
                    duration = leg.duration
                    departure = state.times[leg.airplanes[i]]
                    if leg.arrival.openingTime > arrival:
                        arrival = leg.arrival.openingTime
                        duration = leg.arrival.openingTime - departure
                        departure = leg.arrival.openingTime - leg.duration
                    if ((state.locations[leg.airplanes[i]].name == leg.departure.name)  and (leg.arrival.closingTime > arrival) and leg.departure.closingTime > departure):
                        #actions.append(Action(leg.airplanes[i], leg.arrival, ( duration + self.airplanes[leg.airplanes[i]].rotTime)  , self.maxProfit - state.profit - leg.profits[i], k, leg.profits[i], departure))
                        actions.append(Action(leg.airplanes[i], leg.arrival, ( duration + self.airplanes[leg.airplanes[i]].rotTime)  , 1+leg.maxProfit-leg.profits[i]+(1/(leg.maxProfit-leg.minProfit)), k, leg.profits[i], departure))
                        #print(self.airplanes[leg.airplanes[i]].name, leg.arrival.name, leg.maxProfit-leg.profits[i]+(1/(leg.maxProfit-leg.minProfit)))
            if(leg.departure.name == "NULL"):
                for i in range(0,len(leg.airplanes)):
                    if (state.locations[leg.airplanes[i]].name == leg.departure.name ):
                        actions.append(Action(leg.airplanes[i], leg.arrival, leg.arrival.openingTime , 1+nr_null, k, 0, None))
                        #print(self.airplanes[leg.airplanes[i]].name, leg.arrival.name, nr_null)
            k=k+1

        #input()
        return actions
                    
    def result(self, state, action):
        #print(self.airplanes[action.index].name + ":" + state.locations[action.index].name + "->" + action.arrival.name)
        #input()
        new_state=deepcopy(state)
        new_state.locations[action.index] = action.arrival
        new_state.times[action.index] = (state.times[action.index] + action.duration)
        if(action.profit != 0):
            new_state.legs[action.leg] = 0;
            new_state.profit = new_state.profit + action.profit
        else:
            new_state.initialLocations[action.index] = action.arrival
        
        if(state.locations[action.index].name != "NULL"):
            new_state.solution[action.index] = new_state.solution[action.index] + action.departure.toString() + " " + state.locations[action.index].name + " " + new_state.locations[action.index].name + " " 
            #new_state.solution[action.index] = new_state.solution[action.index] + state.times[action.index].toString() + " " + state.locations[action.index].name + " " + new_state.locations[action.index].name + " " 
       
        #print( new_state.locations[0].name + " " + new_state.locations[1].name)
        return new_state 

    
    def goal_test(self, state):
        
        for l in state.locations:
            for L in state.initialLocations:
                if(L == None):
                   return False
                if(l.name != L.name):
                    return False
                
        for l in state.legs:
            if(l==1):
                return False
                
        return True
    
    def path_cost(self, c, s1, action, s2):
        #return c + action.cost
        return action.cost
    
    def heuristic(self, state):
        return (self.maxProfit - state.state.profit)/self.maxProfit
        #return 0
        
    def load(self, f):
        self.legs = []
        self.airports = []
        self.airplanes = []
        self.classes = []
        A = []
        C = []
        P = []
        L = []
        
        for line in f:
            s=line.split(" ")
            if(s[0]== "A"):
                A.append(s)
            elif(s[0] == "C"):
                C.append(s)
            elif(s[0] == "P"):
                P.append(s)
            elif(s[0] == "L"):
                L.append(s)
                
        for s in A:
            self.airports.append( Airport(s[1], Time(s[2]), Time(s[3])) )
        for s in P:
            self.airplanes.append(Airplane(s[2][0:-1], s[1]))
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
        for s in C:
            for p in self.airplanes:
                if(p.airplaneClass == s[1]):
                    p.setRotTime( Time(s[2]) )
        
        vtimes = []
        vairports = []
        
        for k in range(0,len(self.airplanes)):
            vtimes.append(Time("0000"))
            vairports.append(Airport("NULL", vtimes[0], vtimes[0]))
        
        for k in range(0, len(self.airports)):
            self.legs.append(Leg(vairports[0],self.airports[k], self.airports[k].openingTime, range(0,len(self.airplanes)), [0] * len(self.airplanes)))
        
        self.initial = State(vtimes,vairports, len(self.legs)-len(self.airports), self.airplanes)

                    
    def save(self, f,state):
        k=0;
        for a in state.solution:
            s = a.split(" ")
            if(len(s)>3):
                f.write(a+ "\n")
            print(a)
            k+=1
        f.write("P " + str(state.profit))
        print("P " + str(state.profit))

class State():   

    def __init__(self, times, locations, nrLegs, planes):
        self.initialLocations = [None] * len(planes)
        self.times = times
        self.locations = locations
        self.legs = []
        self.solution = []
        self.profit=0
        
        for i in range(len(planes)):
            self.solution.append("S " + planes[i].name + " ")
            
        for i in range(nrLegs):
            self.legs.append(1) 
      
    def __lt__(self, node):
      return (self.profit<node.profit)
      
class Leg():
    
    def __init__(self, departure, arrival, duration, airplanes, profits):
        self.departure = departure
        self.arrival = arrival
        self.duration = duration
        self.airplanes = airplanes #array de inteiros com o indice do avião no vetor de aviões
        self.profits = profits
        self.maxProfit = max(profits)
        self.minProfit = min(profits)
        if self.maxProfit == self.minProfit:
            self.maxProfit = self.minProfit + 1.1
        

class Airplane():
    
    def __init__(self, airplaneClass, name):
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
    
    def __init__(self, index, arrival, duration, cost, leg, profit, departure):
        self.index = index
        self.arrival = arrival
        self.duration = duration
        self.cost = cost
        self.leg = leg
        self.profit = profit
        self.departure = departure
        
class Time():
    def __init__(self, s):
        self.h = s[0:2]  
        self.m = s[2:4] 

    def __add__(a, b):
        c = Time('0000')
        c.setH( int(a.h) + int(b.h))
        c.setM( int(a.m) + int(b.m))
        
        if(int(c.m) > 59):
            c.setH( int(c.h)+1)
            c.setM( int(c.m)-60)
        
        return c
        
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
        
    def setH(self, h):
        a= str(h)
        if(h<10):
            a = "0" + str(h)
            
        self.h = a
    
    def setM(self, m):
        a=str(m)    
        if(m<10):
            a = "0" + str(m)

        self.m = a
        
    def __gt__(a, b):
        if (int(a.h) > int(b.h)):
            return True
        elif( (int(a.h) == int(b.h)) and (int(a.m) >= int(b.m))):
            return True
        else:
            return False

    def toString(self):
        return self.h + self.m

        