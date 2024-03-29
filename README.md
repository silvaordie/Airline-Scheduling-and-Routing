# Airline Scheduling and Routing

The airline industry is one of the most competitive ones in the world economy. For instance, the pressure of the low-cost airliners pushed the whole industry
to pursue cost efficiency. One critical components of this efficiency is the scheduling and routing of the airplanes, given a set of legs to be flown by the
company. This project addresses the problem of finding the daily schedule and routing of airplanes that maximizes the company profit, hereby called
the Airline Scheduling And Routing (ASAR) problem.

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
For the cost, it is desired to penalize actions that are not the most profitable. Therefore, the cost is defined as the difference between the leg's most profitable airplane and the chosen airplane to execute the leg.
``` cost = leg[i].maxProfit - leg[i].profits[k] #i: leg index, k: airplane index```

As for the heuristic, it is desired to make an estimate of the state's future path costs. If the problem, from the current state to the goal state, flies only the most profitable plane (minimum cost), the future path cost would be the number of legs that are still left to be flown. This heuristic will help the A* algorithm to search in depth for the solution before expanding other nodes that could have the same cost but are more distant to the solution.

# Does the A* algorithm guarantees the optimal solution? #
In order for the A* algorithm to guarantee the optimal solution the heuristic has to be admissible if the search space is a tree, or consistent if the search space is a graph.

Why admissible? Having an admissible heuristic implies that the A* will always expand a node that is in the path to the optimal solution before expanding a node that does not lead to an optimal solution, even if that node is a goal (this is only valid if the costs are strictly positive).

Why consistent? For graphs there are a possibility where two different paths lead to the same node, in this case the A* discards one of the repeated nodes. The consistency guarantees that the A* will never discard the node that is in the path to the optimal goal.

Our cost and heuristic functions do not guarantee the optimal solution of the algorithm, although they are close to it. It would be easy to transform our cost and heuristic in order to fulfill this requirements, the problem is that if we do it, the search will expand much more nodes, requiring a lot more computational time.

# Number of nodes generated, depth of the solution and effective branching factor #

* Example 1: Nodes: 35	Depth: 10 	Effective Branching Factor: 1.4269
* Example 2: Nodes: 47	Depth: 12	Effective Branching Factor: 1.3783 
* Example 3: Nodes: 177	Depth: 8	Effective Branching Factor: 1.9098
* Example 4: Nodes: 71	Depth: 10	Effective Branching Factor: 1.5315
* Example 5: Nodes: 91	Depth: 12	Effective Branching Factor: 1.4563
* Example 6: Nodes: 5598	Depth: 10	Effective Branching Factor: 2.3703
* Example 7: Nodes: 4919	Depth: 10	Effective Branching Factor: 2.3398
* Example 8: Nodes: 252	Depth: 12	Effective Branching Factor: 1.5853

The depth of the solution is fixed for a given input and it is given by the number of legs + number of airplanes in a certain file. This conclusion derives from our formulation of the inital state. In the beginning we assign a null airport to each airplane and we had a leg that makes the airplane go from the null airport to a open airport.

The effective branching factor is aproximately N^(1/d), where N is the number of generated nodes and d is the depth of the solution.

