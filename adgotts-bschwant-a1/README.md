# Part 1: The 2021 Puzzle
Description: Our program uses A* search to find the canonical configuration of a board. In A* search f(s) = g(s) + h(s), where g(s) represents the amount of moves made so far and the heuristic function (h(s)) represents the Manhattan distance of a board from the canonical configuration. To implement this we first convert the board passed into our program into a numpy array. We chose to work with numpy due to its speed, and its ability to easily manipulate rows/columns within its array structure. We used a priority queue as our fringe which stores the cost of a board configuration ( f(s) ), the board configuration, the amount of moves made so far ( g(s) ), and a string representing the letter representation of moves. The state with the lowest cost is removed from the fringe, and its successors are generated. The successors are then added to the fringe, and the board configuration in the fringe with the lowest total cost is again removed. This process continues until the goal state is found or the fringe is empty.

Search Abstraction
- State Space: Given an initial board, all possible configurations of the board that can be reached by the game rules.
- Initial State: A board in a text file passed into the program  
- Successor Function: Given a board, the successors are new boards in which:
  - Column has been moved Up/Down by 1
  - Row has been moved left/right by 1
  - Outermost ring has been rotated counterclockwise/clockwise by 1
  - Innermost ring has been rotated counterclockwise/clockwise by 1.
- Heuristic Function: The sum of the manhattan distances of each number on the board from its goal state. This will never overestimate the cost it takes to get to our goal state, as every number will have to be moved, at minimum, its current distance to the end goal location. Therefore it is admissable. 
- Goal State: The canonical representation of the board

Questions:
- Branching factor: 24
- 7 move solution in BFS instead of A*: If we have a branching factor of 24 and the solution is at a depth of 7. It should take roughly 24^7 = 4,586,471,424 states.

Problems: We had a hard time originally with numpy and generating the different successor states. After reading into the numpy documentation we realized that np.copy() would have to be used to generate the different states due to how numpy is implemented in memory. 

# Part 2: Road trip!

Description: Our search algorithm consists of depth first search of most favorable states in the state space. We implemented our search alogirthm as a priority queue so states with the lowest priority (favorable) were expanded first. States are determined to be favorable if they are located closer to the [end-city] based on the the compute distance between GPS coordinates of the state and the destination and the cost of the move based on the given [cost-function].

Search Abstraction:
- State Space: The state space S for a given node (city) for of our route planning algorithm consists of all cities or road junctions connected by road segments to the node. This includes road segments in which our node is the origin and destionation. Valid states in this space are other nodes that have not been visited yet.
- The succesor function of our planning algorithm returns all eligble states for a given city (or road junction).
- The edge weights for our planning algorithm are computed based on the cost function provided as an input and assigned a weight based on that.
- The goal state of our planning algorithm is the [end-city] given as an input with the minimal cost when running our planner.
- The heuristic function created for this program was the total distance remaining until the [end-city] based on the distance of GPS coordinates. However, the function is not admissable because there are moves to valid states that can increase the cost (distance) to the destination.

Problems, Assumptions, Design Decisions: Initially, our search algorithm was completed depth first search of favorable neighboring states based soley on the cost of a given move based on the [cost-function] provided. This works fine and was able to quickly find a solution when cities are only a few nodes apart (i.e Bloomington and Indianapolis); however, when cities that are further apart are given as the input (i.e Los Angeles and Indianapolis), searching based on the cost of the moves proved to be ineffective. For example, choosing to explore a neighbooring node with the shortest distance road segement is not the best idea when trying to travel accross the country. To account for this, we added distance to the goal to the priority value of states in addition to previously mentioned cost. The priority queue we implemented selects states to explore based on low priority values so states closer geographically to our goal are explored first.
However, some cities and road junctions especially did not have corresponding GPS coordinates. Originally, I found the nearest neighbor with GPS coordinates and used those to calculate distance; howwever, when attempting to find routes accross the country, often times large areas of what appeared to be only road junctions would occur. I found our program fequently got stuck in area like this and I assume this is because the nearest neighbor with GPS coordinates was geographcially further away which resulted in our algorithm to choosing not to explore these states. As a result, we did not add distance to states with no coordinates. I believe this can be both better and worse depending on road configurations. Thes states are then explored first as a result; however, the assumption was made that it would "quickly" explore a neighbor with coordinates and at that point would either continue exploring neighbors, or explore somewhere else with lower priority value (closer to goal).
One final issue with our search alogrithm is also a result of including distance in priority value. Because distance is a much larger value than any of the cost associated with our cost functions, at least initally. (ex. Distance from Los Angeles to Inianapolis is much larger than the time, or distance associated with a corresponding road segment). Because of this, we can only assume that our cost function is largely ignored at the start of searches and has less impact in state selection until distance from goal is decreased. However, without including distance, routes often failed to be found.

# Part 3: Choosing teams

Description: For this problem we decided to implement a uniform cost search. While A* search was also considered, we decided the amount of steps needed to achieve the state with the minimum cost was irrelevant in this situation and should not be factored into the cost.  Our algorithm first organizes the input file into the maximum number of groups to minimize the amount of computational steps needed to reach a minimum cost. From here a priority queue is used as the fringe to store successor functions and their associated cost in a tuple (cost, groups). The successor function with the lowest cost is selected from the queue, and the process repeats. Every time a list of groups is removed from the fringe, our program checks to see if the cost is lower then any of those that came before it. If so we yield the list of groups, and their associated cost. This process repeats until the fringe is empty. 

Search Abstraction
- State Space: All possible configurations of different groups
- Initial State: The amount of groups had the second largest time cost for the teacher, so we decided to make the initial state the state in which all groups are as full as they could be. This minimized the initial cost of the calculation and saved our search algorithm time.
- Successor Function: Figuring out how we wanted to make the successor function for this problem took some time and we tried a few different approaches. In the end we decided to loop through each username in each group, remove the username from the group it was in, and then add it to either a group that was not full or to make a new group of 1. In this case there was (number of groups - full groups)*(number of usernames) successors for each state. 
- Cost: We used what was outlined in the assignment to determine the cost of a group. Each of the elements below were summed for each list of groups:
  - It will take 5 minutes to grade each assignment, so total grading time is 5 times the number of teams.
  - Each student who requested a specific group size and was assigned to a different group size will send
a complaint email to an instructor, and it will take the instructor 2 minutes to read this email.
  - If a student is not assigned to someone they requested, there is a 5% probability that the two students
will still share code, and if this happens it will take 60 minutes for the instructor to walk through the
Academic Integrity Policy with them. If a student requested to work with multiple people, then this
will happen independently for each person they were not assigned to. If both students requested each
other, there will be two meetings.
  - Each student who is assigned to someone they requested not to work with (in question 3 above)
complains to the Dean, who meets with the instructor for 10 minutes. If a student is assigned to a
group with multiple people they did not want to work with, a separate meeting will be needed for each.
- Goal state: The list of groups that results in the mimium value of time for the instructors. The best minimum value currently found is yielded by our program.

Problems: We tried a few different successor functions for our application. Originally we were planning on starting with an empty group list, where each successor would be the placement of one username. Each iteration a new username would be added to a group to minimize the cost. We ended up scrapping this idea halfway through because while it would be both complete and optimal, we did not think it would be able to yield solutions in time. With the successor function we did end up going with, working with popping and inserting elements from a 2D list of groups 
proved to be challenging. Learning was needed to understand how lists are stored in memory, and how to avoid changing the value of a list when modifying a copy of it.  

