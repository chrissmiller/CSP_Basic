# CSP Homework
Chris Miller
---

## Constraint Satisfaction Class
My ConstraintSatisfactionProblem class implemented backtracking on a generic form that any CSP can be converted to - a set of variables, each with their own domain of possible values, and a constraint dictionary which maps from pairs of variables to legal combinations (if no map between two variables exists, they have no constraints on each other, and if an empty list exists, the pair has no legal combinations). 

The primary search function, `backtrack`, calls a helper function, `backtrack_search`, which recursively implements the backtrack search algorithm.

It first validates the assignment, seeing if the assignment is a solution. If not, it gets an unassigned variable via the `get_unassigned` function. 

`get_unassigned` is implemented as finding the first unassigned value by default, but can also pick a random value (which seems to dramatically increase speed when used with inference) or use MRV (which seems to slightly increase speed in some cases).

While there are values remaining in the set of domain values for the variable, it gets one and tries it by seeing if the assignment violates constraints for any previously assigned variables. If it does not, it tries inference (if inference has been enabled) and then backtracks again and selects the next unassigned variable to work on.

If the assignment fails (has no solutions deeper in the tree), the function resets the variable assignments and returns further up the tree, eventually returning false if all assignment attempts fail.

My inference was implemented via the AC-3 algorithm, as described in class. I found that inference always reduced the number of calls to the backtracking function (as expected) but did not always improve time (except with random unassigned variable selection). This suggests that an improvement to inference efficiency would be necessary for it to be a valuable addition.

### Map Solver Problem

#### Constraint Conversion

My map solver takes a description in the following format:
	
	Territory1 Territory2 ... TerritoryN
	Territory1 Constraint1 Constraint2 ... ConstraintN
	Territory2 Constraint1 Constraint2 ... ConstraintN
	...
	TerritoryN Constraint1 Constraint2 ... ConstraintN
	ColorVal1 ColorVal2 ... ColorValN

For the Australia problem, we have the following description:

	WA NT Q NSW V SA T
	WA NT SA
	NT WA SA Q
	Q NT SA NSW
	NSW Q SA V
	V NSW SA
	Red Blue Green

It parses these using python's split method to produce the correct constraints, and sets the domain to all color values for every variable.

#### Testing

I tested on the Australia problem, and produced this correct result: 

	Territory WA is colored Green
	Territory NT is colored Blue
	Territory Q is colored Green
	Territory NSW is colored Blue
	Territory V is colored Green
	Territory SA is colored Red
	Territory T is colored Red

### Circuit Board Problem

#### Discussion Questions
* Describe the domain of a variable corresponding to a component of width w and height h on a circuit board of width n and height m.

The domain of a w by h component on an n by m board is the cartesian product between the x domains and y domains of the component, where the x domain is between 0 and n-w and the y domain is between 0 and m-h. This is because the component needs h spaces above it and w spaces to the right of it to fit properly.

* Consider components a and b above, on a 10x3 board. In your write-up, write the constraint that enforces the fact that the two components may not overlap. Write out legal pairs of locations explicitly.

Component a (3x2) and b (5x2) have valid combinations of locations when their individual locations are in their domain and the two do not overlap. I used an algorithm which determines overlap by checking if either component is below the other or to the right of the other. If neither are true, then the components overlap and the combination violates the constraint that the rectangles not overlap.

This provides the following constraints for the pair (aLocation, bLocation):

	((0, 1), (3, 0))
	((0, 1), (5, 0))
	((0, 1), (4, 0))
	((0, 0), (3, 0))
	((0, 0), (5, 0))
	((0, 0), (4, 0))
	((7, 0), (0, 0))
	((7, 0), (2, 0))
	((7, 0), (1, 0))
	((7, 1), (0, 0))
	((7, 1), (2, 0))
	((7, 1), (1, 0))
	((6, 1), (0, 0))
	((6, 1), (1, 0))
	((6, 0), (0, 0))
	((6, 0), (1, 0))
	((2, 1), (5, 0))
	((2, 0), (5, 0))
	((5, 0), (0, 0))
	((5, 1), (0, 0))
	((1, 0), (5, 0))
	((1, 0), (4, 0))
	((1, 1), (5, 0))
	((1, 1), (4, 0))


* Describe how your code converts constraints, etc, to integer values for use by the generic CSP solver.

My code for the circuit board problem accepts a problem description string in the following format:
	
	Board: (width, height)
	componentSymbol1: (width, height)
	componentSymbol2: (width, height)
	...
	componentSymbolN: (width, height)
	
Where the first line provides the height and width of the circuitboard, and each subsequent line indicates the symbol used to represent the component on the board and the width and height of the component.

My parser separates the input into lines, strips spaces to avoid errors with literal_eval, parses each line using the split() function, and then uses literal_eval to turn the provided (width, height) text into tuples. The component symbols are mapped in a name_map dictionary, and later retrieved when displaying the finished object. 


For the provided problem we input this description:

	Board: (10, 3)
	a: (3, 2)
	b: (5, 2)
	c: (2, 3)
	e: (7, 1)
	
and the backtracking search produces the valid result of:
	
	*eeeeeeecc
	aaabbbbbcc
	aaabbbbbcc

where an asterix is used to show the unused board space.




#### Timing:

I did not test with my random attribute, even though the random attribute dramatically increased average speed with inference. This is because the random attribute increased the range of speeds, rendering timeit unuseful.

Testing board:

	Board: (17, 3)
	a: (10, 2)
	b: (5, 2)
	c: (2, 3)
	e: (7, 1)

No inference or MRV:
	20.4 ms execution
	
Both:
	783 ms execution
	
Just MRV:
	150 ms execution
	
Just inference:
	567ms execution
	
	
MAP
Australia problem, RGB domain

No inference or MRV:
	1.54 ms execution	
	
Inference and MRV:
	2.96 ms execution

Just inference:
	3.02 ms execution
	
Just MRV:
	1.44 ms execution
	

	
## Min-Conflicts
I also implemented the min-conflicts algorithm.

I followed the pseudocode laid out in the textbook for this. This included a basic min-conflicts function, which loops for a given number of times (max_steps) while attempting to solve the problem. It begins with a random assignment of all variables via the `assign` function, then for every iteration checks if the current assignment is a solution via the `validate` function. 

If the current assignment is invalid, the function sets a conflict table, which calculates the number of conflicts every variable has with other variable assignments (ie, how many constraints each variable assignment violates). It then pulls a random variable which has a conflict via the `get_conflicted` function, and then assigns it the value that minimizes conflicts.

This actually works extremely efficiently, with noticeably faster execution for many problems, especially problems with many solutions (such as a circuitboard with multiple open spaces). Although irregular timing for poor initial assignments caused problems using the timeit module, measuring iterations shows that the algorithm sometimes took as few as 4 steps to assign to the 17x3 grid!

However, the algorithm has a clear downside - a bad initial assignment can cause the algorithm to fail or take a long time. In testing, the best runs on the 17x3 test board used above took under 7 milliseconds - barely a third of the time that backtracking took. However, the worst case runs (where the algorithm failed to find a solution in the 30,000 iterations I gave it) took 3.31 seconds to fail.

Its use to some degree also relies on knowing a solution exists - otherwise, we might increase max_steps and continue waiting for a solution when none exists. Backtracking, on the other hand, is guaranteed to fail and inform us that no solution is present.