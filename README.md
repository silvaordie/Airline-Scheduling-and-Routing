A state is represented by the spatial and temporal locations of each of the problem's airplanes and also by the legs that have already been completed.

Before explaining the state representation, it is necessary to define how the Problem's variable's are stored. The class ASARProblem has the following attributes:
	* legs: Vector of object of the type "Leg" loaded form the input file
	* airports: Vector of objects of type "Aiport" loaded from the input file
	* airplanes: Vector of objects of type "Airplane" loaded from the input file
    * classes: Vector of objects of type "Airplane" loaded from the input file

With this in mind, a state is represented by an Object of type "State" with the following attributes:
    * initialLocations: Vector of objects of type "Airport", State.initialLocations[i] stores the starting airport of ASARProblem.airplanes's i'th plane
    * times: Vector of objects of type "Time", times[i] stores the time location of ASARProblem.airplanes's i'th plane
    * locations: Vector of objects of type "Airport", State.locations[i] stores the location of ASARProblem.airplane's i'th plane, in the time instant State.times[i]
    * legs: Vector of booleans (0 or 1), if legs[i]==1 means that the ASARProblem.legs[i] has not yet been made, else the leg as already been completed
    * solution: Vector of strings containing the spatial and temporal path of ASARProblem.airplanes[i] plane in the format "S <airplane.name> <time1> <dep1.name> <arr1.name> <time2.name> <dep2.name>"
    * profit: Float with the cumulative profit of all of the state's completed legs

A state operation consists in moving a single plane from it's current airport if there's a leg that allows it to do so (Leg that departs on the current airport , and arrives to the destination while both airports are still open). Also, when a plane is moved, it's current time is updated to (previoustime + leg.duration + airplane.rotationTime). The operations are represented by Objects of type "Action", with the following atributes:
    -index: Position of the travelling airplane in the State.Airplanes vector
    -arrival: Object of type "Airport" to which the plane is traveling to
    -duration: "Time" Object with the duration of the Leg journey
    -cost: The cost of executing the action
    -leg: Position of the leg that generated the action in the State.legs vector
    -profit: Profit gained from executing the action
    -departure: Object of type "Airport" in which the plane will depart from