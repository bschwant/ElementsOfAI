#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: adgotts, bschwant
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np
from queue import PriorityQueue
import re

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

def successors(state, move_list):
    ''' Returns a list of possible successor states'''
    
    successors = []

    # Each numpy array has its own place in memory, we need to copy it
    s_oc = np.copy(state) # Outer Clockwise
    s_occ = np.copy(state) # Outer Counter-Clockwise
    s_ic = np.copy(state) # Inner Clockwise
    s_icc = np.copy(state) # Inner Counter-Clockwise


    for i in range(0,5):
        s_u = np.copy(state)
        s_d = np.copy(state)
        s_r = np.copy(state)
        s_l = np.copy(state)

        s_u[:, [i]] = np.roll(s_u[:, [i]],-1, axis=0) # Up
        s_d[:, [i]] = np.roll(s_d[:, [i]],1, axis=0) # Down
        s_r[i] = np.roll(s_r[i], 1) # right
        s_l[i] = np.roll(s_l[i], -1) # left

        if (i == 0): # Clockwise / Counter Outer
            s_oc[i] = s_r[i]
            s_oc[:, [i]] = s_u[:, [i]]

            s_occ[i] = s_l[i]
            s_occ[1:, [i]] = s_d[1:, [i]]

        if(i == 4): # Clockwise / Counter Outer
            s_oc[i] = s_l[i]
            s_oc[1:, [i]] = s_d[1:, [i]]

            s_occ[i][1:] = s_r[i][1:]
            s_occ[:4, [i]] = s_u[:4, [i]]
            
        if(i == 1): # Clockwise / Counter Inner
            s_ic[i][1:4] = s_r[i][1:4]
            s_ic[1:3, [i]] = s_u[1:3, [i]]

            s_icc[i][1:4] = s_l[i][1:4]
            s_icc[2:4, [i]] = s_d[2:4, [i]]

        if(i == 3): # Clockwise / Counter Inner
            s_ic[i][1:4] = s_l[i][1:4]
            s_ic[2:4, [i]] = s_d[2:4, [i]]

            s_icc[i][2:4] = s_r[i][2:4]
            s_icc[1:3, [i]] = s_u[1:3, [i]]
            
        successors.append((s_u, move_list + f'U{i+1}'))
        successors.append((s_d, move_list + f'D{i+1}'))
        successors.append((s_r, move_list + f'R{i+1}'))
        successors.append((s_l, move_list + f'L{i+1}'))
    
    successors.append((s_oc, move_list + 'Oc'))
    successors.append((s_occ, move_list + 'Occ'))
    successors.append((s_ic, move_list + 'Ic'))
    successors.append((s_icc, move_list + 'Icc'))
    
    assert(len(successors) == 24)

    return successors

def heuristic(state):
    ''' Given a state, calculate the sum of the Manhatten distance to the goal state'''

    # Create Solution Matrix
    solution = np.arange(1,26)
    solution = np.reshape(solution,(5,5))

    # Calculate Manhatten Distance
    sum = 0
    for i in range(1, 26): # doesnt include wrap around
        a,b = tuple(np.where(state == i)) # returns coordinates in matrix of i location
        c,d = tuple(np.where(solution == i))
        sum = sum + np.abs(a-c) + np.abs(b-d)
    
    return sum

def is_goal(state):
    '''  Check if we've reached the goal'''
    
    # Create Solution Matrix
    solution = np.arange(1,26)
    solution = np.reshape(solution,(5,5))

    if np.array_equal(solution,state):
        return True
    else:
        return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    id = 0 # unique ID that acts as a tie breaker for the priority queue
    closed = [] # contains used states
    
    # Convert initial board into a numpy matrix
    print(initial_board)
    initial_board = np.reshape(initial_board,(5,5)) 
    
    # Initialize Fringe 
    fringe = PriorityQueue()
    fringe.put((0, id, initial_board, 0, "")) # ((g(x) + h(x)), state, g(x), move_str)

    while not fringe.empty():
        _, _, state, gx, move_list = fringe.get()

        s_list = successors(state, move_list)
        for state in s_list:
            id += 1 # give each state a unique ID
            h = heuristic(state[0]) # Manhatten Distance
            if is_goal(state[0]):
                move_string = re.sub( r"([A-Z])", r" \1", state[1]).split()
                return move_string
            fringe.put(((h+gx), id, state[0], (gx+1), state[1]))

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
