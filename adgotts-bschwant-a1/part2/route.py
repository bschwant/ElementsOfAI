#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Brian Schwantes -  bschwant 
#

# !/usr/bin/env python3
import sys
import numpy as np
from queue import PriorityQueue
import math

def find_nearest_cord(next_city, city_cords, all_roads):

    closest_dist = 1000.0
    closest_cords = None
    for road in range(0, len(all_roads)):
        if(all_roads[road][0]==next_city):
            if(city_cords.get(all_roads[road][1]) and float(all_roads[road][2]) < closest_dist):
                iclosest_cords = city_cords[all_roads[road][1]]
        elif(all_roads[road][1]==next_city):
            if(city_cords.get(all_roads[road][0]) and float(all_roads[road][2]) < closest_dist):
                closest_cords = city_cords[all_roads[road][0]]
    return closest_cords

            

def get_coordinate_dict():

    city_file = open('city-gps.txt', 'r')
   
    cities={}

    for line in city_file:
        temp = line.split(" ")
        city = temp[0]
        lat = temp[1]
        lon = temp[2]
        
        cities[city] = (lat, lon)
    
    return cities

'''
    Code to calculate distance between coordinates from:
    https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
'''
def get_distance (city_cord, start_cord, end_cord):
    lat_c, lon_c = float(city_cord[0]), float(city_cord[1].replace("\n",""))
    lat_s, lon_s = float(start_cord[0]), float(start_cord[1].replace("\n",""))
    lat_e, lon_e = float(end_cord[0]), float(end_cord[1].replace("\n",""))
    R = 6373.0

    # Starting distance
    lat1, lon1 = lat_s, lon_s # origin
    lat2, lon2 = lat_e, lon_e #destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    original_dist = d
    # current dist
    lat1, lon1 = lat_c, lon_c # origin
    lat2, lon2 = lat_e, lon_e #destination
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    current_dist = d
    distance = original_dist - current_dist
    #distance_priority = 5000-distance    # makes states closer to finish more favorable
    #distance_priority = distance_priority * .01
    return current_dist


# Get list of succesors based on current city
def successors(curr_city, all_roads):

    next_cities = []
    
    # Get all roads from curr_city
    for road in range(0, len(all_roads)):
        #print(all_roads[road][0])
        if(all_roads[road][0]==curr_city):
            from_city = all_roads[road][0]
            to_city = all_roads[road][1]
            seg = 1
            dist = all_roads[road][2]
            speed = all_roads[road][3]
            road_name = all_roads[road][4]
            
            time = float(dist)/float(speed)
            del_time = time

            next_cities.append((int(seg), float(dist), float(time),float(del_time), road_name, to_city,speed))
    # Get all roads to curr_city
        elif(all_roads[road][1]==curr_city):
            from_city = all_roads[road][1]
            to_city = all_roads[road][0]
            seg = 1
            dist = all_roads[road][2]
            speed = all_roads[road][3]
            road_name = all_roads[road][4]

            time = float(dist)/float(speed)  # use minute so time matters more
            del_time = time

            next_cities.append((int(seg), float(dist), float(time),float(del_time), road_name, to_city,speed))
    return next_cities
        
    # Get all roads to curr_city
    
# Create list of roads to search based starting locaiton
def create_road_list():

    road_file = open('road-segments.txt', 'r')

    all_roads = []

    # example line from file Abbot_Village,_Maine Bingham,_Maine 24 45 ME_16
    for line in road_file:
        split_line = line.split(" ") #Parse line splitting data where there is a space char

        # Check if list of split line contains all elements
        # NOTE: Not sure if this is proper error handling for these cases
        if(len(split_line) != 5):
            continue 

        from_city = split_line[0]
        to_city = split_line[1]
        dist = split_line[2]
        speed_limit = split_line[3]
        road_name = split_line[4]
        list_entry = (from_city, to_city, dist, speed_limit, road_name)

        all_roads.append(list_entry)

    return all_roads


# Helper function to create dictory to be returned
def create_return_dict(segments, distance, time, delivery, route):

    final_route = []

    temp_route = route.split(">")

    for i in temp_route:
        if(i):
            temp_path = i.split("|")
            road_dist = temp_path[1].split("<")
            temp_road_dist = str(road_dist[0]).replace("\n", "") + " for "+str(road_dist[1]) + " miles"
            final_route.append((temp_path[0], temp_road_dist))
   
    time = time  # convert back to hours
    return_dict = {"total-segments" : segments,
            "total-miles" : distance,
            "total-hours" : time,
            "total-delivery-hours" : delivery,
            "route-taken" : final_route}
    return return_dict
''' 
    -Function to get route between user input
       start and end cities based on given cost function.
        
    -Possible cost functions:
        -segments, distance, time, delivery 
    
    -INPUT: start city, end city, cost function

    -Return: dictionary with the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
           it will take a delivery driver who may need to return to get a new package
'''
def get_route(start, end, cost):
    
    # Variable to track one program finds starting city 
    city_found = False

    # Check if start city is contained in road segement file
    all_roads = create_road_list()
    city_check = False

    for i in range (0, len(all_roads)):
        if(all_roads[i][0] == start):
            city_check = True

    if(city_check == False):
        print("City is not a starting city in road-segments.txt")
    else:
        print("\n\nCITY FOUND")

    city_coords = get_coordinate_dict()

    start_coords = city_coords[start]
    end_coords = city_coords[end]

    # Check if start city is in city-gps.txt and find near by cities



    # List to store visited cities
    visited_cities= []

    # Create fringe to store nodes (cities) to be explored
    # Uses priority queue over queue so nodes that are favorable for given cost type  are explored first 
    fringe = PriorityQueue()

    # Create first entry into queue, with in form below, and add it to queue 
    # (<node_priority>,<tot segs>,<tot dist>,<tot time>,<delivery>,<current city>)
    route_taken = ""
    first_entry = (0,0,0,0,0,"",start)
    fringe.put(first_entry)

    route = {}
    list_route = [None]*20
    visited_cities.append(start)
    solution = False
    while fringe:
        
        (node_priority,all_segments,tot_distance,tot_time,tot_delivery,this_route,curr_city) = fringe.get()
        
        for (segments,distance,time,delivery,road_name,next_city,speed) in successors(curr_city,all_roads):
            
            temp_route = str(this_route)+">"+ str(next_city)+"|"+str(road_name)+"<"+str(distance)
            temp_route = temp_route.replace("\n", "")
            
            if(next_city == end):
                this_route = temp_route
                segs = all_segments+1
                dist = tot_distance+distance
                time = tot_time + time
                del_time = tot_delivery + delivery
                temp_return = create_return_dict(segs, dist, time, del_time, this_route) 
                return temp_return

            if(next_city not in visited_cities):
                print("Next City",next_city)                
                visited_cities.append(curr_city)

                # Add priority value based on cost function
                cost_of_step = 0
                # Add additional segment 
                if(cost == "segments"):
                    cost_of_step = all_segments +1
                # Add miles to total distance
                elif(cost == "distance"):
                    cost_of_step = tot_distance + distance
                # Add time to total time
                elif(cost == "time"):
                    cost_of_step = tot_time + time
                # add time to total delivery time
                # needs to be update accoridng to specs
                elif(cost == "delivery"):
                    prob_mistake = math.tanh(float(distance)/1000)
                    if(int(speed)>50):
                        print("SPEED")
                        add_time = prob_mistake * 2 * (time + tot_time)
                        cost_of_step = time + add_time
                        delivery = time + add_time
                    else:
                        cost_of_setp = tot_time + time
                else:
                    return False
                dist = 0 
                if(city_coords.get(next_city)):
                    curr_coords = city_coords[next_city]
                else:
                    nearest = find_nearest_cord(next_city, city_coords, all_roads)
                    #curr_coords = nearest
                dist = 0
                if(curr_coords != None):
                    dist = get_distance (curr_coords, start_coords, end_coords)
                #print("Distance:", dist)
                temp_segs = all_segments+1
                temp_dist = tot_distance+distance
                temp_time = tot_time+time
                temp_del = tot_delivery+delivery
                dist = int(dist)
                cost_of_step+=dist
                #print(cost_of_step)
                fringe.put((cost_of_step, temp_segs, temp_dist,temp_time, temp_del,temp_route,next_city))
            else:
                print("VISITED")
       
    return False


    '''
    route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : 51., 
            "total-hours" : 1.07949, 
            "total-delivery-hours" : 1.1364, 
            "route-taken" : route_taken}
    '''

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


