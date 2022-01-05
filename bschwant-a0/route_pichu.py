#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Brian Schwantes
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]


# Helper function to convert list of moves to a string
def list_to_string(move_list, path_len):
    new_str = ""

    count = 0
    for i in move_list:
        if count > path_len:
            return new_str
        if i != None:
            new_str += i
        count+=1

    return new_str


# Function to create move string from all moves
def find_move_string(moves, num_moves):
    
    actual_moves = [None]*int(num_moves+2)
    move_str = []
    for i in range (0, len(moves)):
        index = moves[i][1]
        if(index > num_moves+1):
            continue
        actual_moves[index] = moves[i][0]
    for i in range(1, len(actual_moves)):
        r_move = actual_moves[i][0] - actual_moves[i-1][0]
        c_move = actual_moves[i][1] - actual_moves[i-1][1]
        
        if (r_move < 0):
            move_char = 'U'
        elif (r_move > 0):
            move_char = 'D'
        elif (c_move < 0):
            move_char = 'L'
        elif (c_move > 0):
            move_char = 'R'

        move_str.append(move_char)

    new_move_str = list_to_string(move_str, num_moves)
    return new_move_str


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)
def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0)]
        move_str = ""
        move_count = 0
        visited = set()
        all_moves = []

        if (house_map[pichu_loc[0]][pichu_loc[1]] == "@"):
            return (0, move_string)

        while fringe:
            (curr_move, curr_dist) = fringe.pop()
            possible_moves = moves(house_map, *curr_move)

            all_moves.append((curr_move, curr_dist))
            
            for move in possible_moves:
                if house_map[move[0]][move[1]]=="@":
                    all_moves.append((move,curr_dist+1))
                    move_str = find_move_string(all_moves, curr_dist)
                    return(curr_dist+1, move_str)
                else:
                    if move not in visited:
                        fringe.append((move, curr_dist+1))
                        visited.add(move)
                     
                    else:
                        continue


# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

