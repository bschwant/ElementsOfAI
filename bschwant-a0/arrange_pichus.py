#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Brian Schwantes
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys
import numpy as np

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0]))
            if house_map[r][c] == '.' and valid_spot(house_map,r,c) ]

# check if house_map is a goal state
def is_goal(house_map, k):
    pichus = count_pichus(house_map)
    print("#:",pichus)
    if pichus> k:
        exit(1)
    if count_pichus(house_map) == k:
        return True #count_pichus(house_map) == k 
        
    else:
        False

def valid_spot(house_map,r,c):
    return check_row(house_map,r,c) and check_column(house_map,r,c) and check_diag(house_map,r,c)

# Check row for multiple pichus within line of sight
def check_row(house_map,r,c):
    
    pichu = False
    wall = False

    row_len = len(house_map)
    temp_row = []
    
    # Add row to temp list
    for i in range(0, row_len):
        if i == r:
            temp_row.append('p')
        else:
            temp_row.append(house_map[i][c])

    # Check row for repeat pichus
    for i in range(0, row_len):
        if temp_row[i] == 'p':
            # Check for previous pichu
            if pichu == True:
                return False
            else:
                pichu = True
        elif temp_row[i] == 'X':
            pichu = False
            wall = True
    return True

# Check column for multiple pichus within line of sight
def check_column(house_map,r,c):

    pichu = False
    wall = False

    col_len = len(house_map[0])
    temp_col = []

    # Add row to temp list
    for i in range(0, col_len):
        if i == c:
            temp_col.append('p')
        else:
            temp_col.append(house_map[r][i])

    # Check row for repeat pichus
    for i in range(0, col_len):
        if temp_col[i] == 'p':
            # Check for previous pichu
            if pichu == True:
                return False
            else:
                pichu = True
        elif temp_col[i] == 'X':
            pichu = False
            wall = True
    return True

# Function checks diagonals for valid moves
def check_diag(house_map,r,c):
    num_pichu = 0
    temp_house_map = np.empty_like(house_map)
    
    for i in range (0,len(house_map)):
        for j in range (0, len(house_map[0])):
            temp_house_map[i][j] = house_map[i][j]

    
    temp_house_map[r][c] = 'p'

    offset = c-r
    offset2 = (len(house_map[0])-1-r)-c
    house = np.array(temp_house_map)
    flipped_house = np.fliplr(house)
    diag_down = house.diagonal(offset)
    diag_up = flipped_house.diagonal(offset2)
  
    sum_pichu = 0
    for i in range(0, len(diag_down)):
        if(diag_down[i] == 'p'):
            sum_pichu +=1
        elif(diag_down[i] == 'X'):
            sum_pichu = 0

        if(sum_pichu>1):
            print("Bad diag down")
            return False

    sum_pichu = 0
    for i in range(0, len(diag_up)):
        if(diag_up[i] == 'p'):
            sum_pichu +=1
        elif(diag_up[i] == 'X'):
            sum_pichu = 0

        if(sum_pichu>1):
            print("Bad diag down")
            return False


    return True

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


