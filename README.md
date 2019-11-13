# Sate representation and operators #
A state is represented by the spatial and temporal locations of each of the problem's airplanes and also by the legs that have already been completed.

Before explaining the state representation, it is necessary to define how the Problem's variable's are stored. The class ASARProblem has the following attributes:
* **legs**: Vector of object of the type "Leg" loaded form the input file
* **airports**: Vector of objects of type "Aiport" loaded from the input file
* **airplanes**: Vector of objects of type "Airplane" loaded from the input file
* **classes**: Vector of objects of type "Airplane" loaded from the input file

With this in mind, a state is represented by an Object of type "State" with the following attributes:
* **initialLocations**: Vector of objects of type "Airport", State.initialLocations[i] stores the starting airport of ASARProblem.airplanes's i'th plane
* **times**: Vector of objects of type "Time", times[i] stores the time location of ASARProblem.airplanes's i'th plane
* **locations**: Vector of objects of type "Airport", State.locations[i] stores the location of ASARProblem.airplane's i'th plane, in the time instant State.times[i]
* **legs**: Vector of booleans (0 or 1), if legs[i]==1 means that the ASARProblem.legs[i] has not yet been made, else the leg as already been completed
* **solution**: Vector of strings containing the spatial and temporal path of ASARProblem.airplanes[i] plane in the format "S <airplane.name> <time1> <dep1.name> <arr1.name> <time2.name> <dep2.name>"
* **profit**: Float with the cumulative profit of all of the state's completed legs

A state operation consists in moving a single plane from it's current airport if there's a leg that allows it to do so (Leg that departs on the current airport , and arrives to the destination while both airports are still open). Also, when a plane is moved, it's current time is updated to (previoustime + leg.duration + airplane.rotationTime). The operations are represented by Objects of type "Action", with the following atributes:
* **index**: Position of the travelling airplane in the State.Airplanes vector
* **arrival**: Object of type "Airport" to which the plane is traveling to
* **duration**: "Time" Object with the duration of the Leg journey
* **cost**: The cost of executing the action
* **leg**: Position of the leg that generated the action in the State.legs vector
* **profit**: Profit gained from executing the action
* **departure**: Object of type "Airport" in which the plane will depart from

# Cost and heuristic functions #
For the cost, it is desired to penalize actions that are not the most profitable. Therefore, the cost is defined as the difference between the leg's most profitabble airplane and the chosen airplane to execute the leg, the + 1  is to guarantee the consitency of our representation, as it is explained below about the heuristic.
``` cost = 1 + leg[i].maxProfit - leg[i].profits[k] #i: leg index, k: airplane index```

As for the heuristic, it is desired to make an estimate of the state's future path costs. To guarantee that the A* algorthm finds the optimal solution, the heuristic function must guarantee the consitency of the A* algorithm, i.e. it must satisfy the following triangular inequality ``` h(n) ≤ c(n,a,n’) + h(n’)``` (for any node n' successor of n using action a). Bearing this in mind, our heuristic is the number of legs that were not completed yet. Considering that we are in a state where x legs were already flown, the hueristic would be N-x, where N is the total number of legs, the cost to go to a successor state would be 1+(leg.maxProfit-leg.profit) and the heuristic of the successor state would be N-x-1 because one more leg was completed. Checking the triangular inequality we have:
```N-x ≤ 1 + (leg.maxProfit-leg.profit) + N-x-1 = N-x + (leg.maxProfit-leg.profit)```
Since leg.profit ≤ leg.maxProfit the inequality is always verified, so our heuristic guarantees the consistency of the A* algorithm.
