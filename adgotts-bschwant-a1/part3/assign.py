#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: adgotts, bschwant
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

from os import name, stat_result
import sys
import time
from queue import PriorityQueue

def readfile(filename):
    ''' Parses the filename into a 2d dictionary with {'username', {group members, group size, blocked members}, ..}'''

    group_list = {}

    f = open(filename,'r')
    survey = f.readlines()
    for line in survey:
        entries = line.split()

        # put group member names into list
        member_name_list = entries[1].split('-') 
        member_names = [name for name in member_name_list if ('xxx' or 'zzz') not in name] # remove 'xxx'/'zzz' from name list

        # Put blocked member names into list
        blocked = entries[2].split(',')

        group_list[entries[0]] = {"group": member_names, "size": len(member_name_list), "blocked": blocked}

    return group_list

def initialize(group_list):
    ''' Build the initial state where every user is already in a group of 3. This minimizes initial group cost'''

    inital_groups = []
    group = []
    for count, entry in enumerate(group_list, 1):
        group.append(entry)
        if count % 3 == 0 or count == len(group_list):
            inital_groups.append(group)
            group = []

    return inital_groups

def cost(groups, form_list):
    ''' Given a group, find the total cost/time of the configuration'''

    time = len(groups)*5 # +5 minutes for each group
    
    for group in groups:
        for username in group:

            # Check for wrong group size. +2 min if in wrong group
            if form_list[str(username)]['size'] != len(group):
                time = time + 2
                
            # Check for requested members in group. +3 min per
            matching_group = set(group).intersection(form_list[str(username)]['group'])
            if (len(matching_group) != len(form_list[str(username)]['group'])):
                time = (time + (3*abs(len(matching_group) - len(form_list[str(username)]['group']))))

            # Check for blocked members in group. +10 min per
            blocked_members = set(group).intersection(form_list[str(username)]['blocked'])
            time = time+(10*(len(blocked_members)))

    return time

def successors(groupls):
    ''' Given a 2D list of groups, calculate possible successor groups '''

    successors = []

    for group in groupls:
        for username in group:
                     
            # Move to other rows if rows are not full
            for i in range(0, len(groupls)):
                if len(groupls[i]) < 3 and groupls[i] != group:
                    new_groupls = [row[:] for row in groupls] # Create a copy of the group_list 2D array
                    from_group = new_groupls[new_groupls.index(group)] # Find where the current group is in the copy of the 2D array
                    new_groupls[i].insert(0, from_group.pop(from_group.index(username))) # Swap positions with new group
                    # Delete if group is empty
                    if not from_group:
                        new_groupls.remove(from_group)
                    successors.append(new_groupls)

            # Move to a new list
            if len(group) != 1: # Dont create a new list if the list already only has 1 person
                new_group  = [username]
                new_groupls = [row[:] for row in groupls] # Create a copy of the group_list 2D array
                from_group = new_groupls[new_groupls.index(group)] # Find where the current group is in the copy of the 2D array
                from_group.pop(from_group.index(username)) # Swap positions with new group
                new_groupls.append(new_group)
                successors.append(new_groupls)

    return successors

def output_format(state):
    ''' Given a 2D list of groups, return the groups in the desired output format''' 
    output = []
    for group in state:
        str1 = '-'.join(group)
        output.append(str1)
    
    return output

def sort_groups(state):
    ''' Sorts the group list, making it easier to check for repeated states'''

    for group in state:
        group.sort()
    state.sort()

    return state

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    # Read From File, and Initialize Starting State and Cost
    form_list = readfile(input_file)
    initial_group = initialize(form_list)
    initial_group = sort_groups(initial_group)
    initial_cost = cost(initial_group, form_list)

    # Initialize Fringe
    fringe = PriorityQueue()
    fringe.put((initial_cost, initial_group)) # ((cost, initial group))    
    
    # Remove Duplicate States
    previous_groups = []
    previous_groups.append(initial_group)

    best_cost = initial_cost

    while not fringe.empty():
        state_cost, group_list = fringe.get()
        
        # Track state data, yield best
        previous_groups.append(group_list)
        if best_cost > state_cost:
            best_cost = state_cost
            yield({"assigned-groups": output_format(group_list),
               "total-cost" : best_cost})

        
        # Loop through successors    
        s_list = successors(group_list)
        for state in s_list:
            state = sort_groups(state)
            scost = cost(state, form_list) # Time
            if state not in previous_groups:
                previous_groups.append(state)
                fringe.put((scost, state))
     

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
