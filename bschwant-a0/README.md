# a0 Brian Schwantes

## Part 1: Navigation
The route_pichu program often fails to find a solution because the starter code failed to track states that had been visited previously and would allow pichu to get stuck going back and forth between two states in the map depending on the order the states are explored. This program uses breadth first search as its search algorithm. It is important to not those elements are added and removed from the fringe on the same side, not opposite. 

- For this program the valid states are spaces above/below/left/right of the agent that are not walls marked by 'X'.
- The succesor function is the next states for a given move. 
- The cost function is irrelvant because all states have the same cost.
- The goal state definition is to reach the postion of the '@'
- The inital state is current pichu location 'p'

In order to fix this pogram, I had to track which states pichu had already visited. Pichu would no longer explore these states if they appeared as possible moves. I tracked these visited states in a list set. In order to produce a string of moves pichu followed to the goal, I tracked all moves and and their respesctive current distance in another list which I went through after reaching the goal to produce the move string.

## Part 2: Hide-and-seek
In order to make the arrange_pichu program work correctly, I implemented the rules that no pichu agents can be visible to each other in the same row and column. In order to have the program run as quickly as possible, the depth first search algorithm was used to find all possible states for a new pichu before adding another. The possible states for a new pichu is any open space '.' that is not visible to another pichu in the same row, column or diagonally. The initial state is one pichu on the map, the goal state is to place 'k' pichus not visible to another pichu. The succesor funtion is a list of the possible spaces for an given pichu to be added. Cost function?
