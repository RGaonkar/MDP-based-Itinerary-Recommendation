#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TO DO : add user preference factor in this

import pickle
import numpy as np
import random
from math import radians, cos, sin, asin, sqrt
import operator

# for split in range(0, 10):
# reading in the input
actions = pickle.load(open("tt" + "/history_2" + "/actions.p", "rb"))
states = pickle.load(open("tt" + "/history_2" + "/states.p", "rb"))
utility = pickle.load(open("tt" + "/history_2" + "/utilities.p", "rb"))
policy = pickle.load(open("tt" + "/history_2" + "/policy.p", "rb"))
place_for_action = pickle.load(open("tt" + "/history_2" + "/action_places_list.p", "rb"))
name_to_coord = pickle.load(open("name_to_coord.p", "rb"))  #for each place name have a list of location coordinates
coord_to_name = pickle.load(open("coord_to_name.p", "rb"))

# print actions
# print states
# print utility
# print policy
	
def get_loc_coordinate():

	global name_to_coord

	import sqlite3
	conn = sqlite3.connect("/home/rad/munich2.db")
	c = conn.cursor()
	
	c.execute("SELECT latitude, longitude, place_name FROM geo_tags")
	conn.commit()

	loc_data = c.fetchall()
	conn.commit()

	# remove repetitions
	loc_data = list(set(loc_data))

	for loc in loc_data:

		try:
			name_to_coord[loc[2]].append((loc[0], loc[1])) 

		except Exception, e:
			name_to_coord[loc[2]] = [(loc[0], loc[1])]
		
		coord_to_name[(loc[0], loc[1])] = loc[2]		
							


def euclidean_distance(place1, place2):

    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # print place1
    lat1 = float(place1[0])
    lon1 = float(place1[1])
    lat2 = float(place2[0])
    lon2 = float(place2[1])

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000 # Radius of earth in meters. Use 3956 for miles
    
    return c * r	


def get_best_place(start_place, place_list):
	# print name_to_coord
	start_coord = random.choice(name_to_coord[start_place])
	place_list_coord = [random.choice(name_to_coord[p]) for p in place_list if p in name_to_coord]

	least_distance = float("inf")
	least_dist_place = ''

	for i in range(len(place_list_coord)):
		
		current_place = place_list_coord[i]

		distance = euclidean_distance(start_coord, place_list_coord[i])

		if distance < least_distance:

			least_distance = distance

			least_dist_place = current_place

	# print least_dist_place
	return coord_to_name[least_dist_place]


def get_best_place_sequence(start_place, action):
	
	place_list = list(set(place_for_action[action]))   #get all the places corresponding to the action

	# #convert the start place to start coordinate
	# start_coord = random.choice(name_to_coord[start_place])
	
	# #convert the place list to list of coordinates 
	# place_list_coord = [random.choice(name_to_coord[p]) for p in place_list if p in name_to_coord]


	###########NEW######################
	start_coord_list = [(float(p[0]), float(p[1])) for p in name_to_coord[start_place]]   #get all the location coordinates corresponding to the place name of start place

	start_coord_list_lat, start_coord_list_lon = zip(*start_coord_list)   #separate out the latitude and longitudes of the start place

	start_coord_avg = (sum(start_coord_list_lat)/len(start_coord_list_lat), sum(start_coord_list_lon)/len(start_coord_list_lon))  #get the average of the latitudes and the longitudes for the start place

	place_list_coord_avg = list()   #list to hold the averaged out coordinates for each of the place names

	avg_coord_to_name = dict()   #dict to hold the place name for the averaged out coordinates

	#for each place corresponding to the action
	for each_place in place_list:
	
		each_place_coord_list = [(float(p[0]), float(p[1])) for p in name_to_coord[each_place]]  #get the list of location coordinates   
		each_place_coord_list_lat, each_place_coord_list_lon = zip(*each_place_coord_list)   #separate out the latitudes and longitudes
		each_place_coord_avg = (sum(each_place_coord_list_lat)/len(each_place_coord_list_lat), sum(each_place_coord_list_lon)/len(each_place_coord_list_lon))
		
		avg_coord_to_name[each_place_coord_avg] = each_place #add the average coordinate and the corresponding place name in a dictionary to be used later
		place_list_coord_avg.append(each_place_coord_avg) #append it to the list of average coordinates for all places corresponding to the action


	place_distance_index = list()   #list to hold the distances 

	place_distance_index = [euclidean_distance(start_coord_avg, place_coord) for place_coord in place_list_coord_avg]

	#add indices to this list to keep track of the relevant place coordinate
	place_distance_index = [(i, distance) for i, distance in enumerate(place_distance_index)]

	place_distance_index.sort(key=operator.itemgetter(1))

	#replace place distance with the place coordinate and then name

	place_distance_index = [(avg_coord_to_name[place_list_coord_avg[dist[0]]], dist[1]) for dist in place_distance_index]
	# print place_distance_index[:5]
	#retain only the place names from this list
	place_name_list = zip(*place_distance_index)[0]
	# print len(place_list)
	# print place_distance_decrease
	# print place_distance_decrease
	# print place_name_list[:5]
	return place_name_list



	####################################


	# place_distance_index = list()   #list to hold the distances 

	# place_distance_index = [euclidean_distance(start_coord, place_coord) for place_coord in place_list_coord]

	# #add indices to this list to keep track of the relevant place coordinate
	# place_distance_index = [(i, distance) for i, distance in enumerate(place_distance_index)]

	# place_distance_index.sort(key=operator.itemgetter(1))

	# #replace place distance with the place coordinate and then name

	# place_distance_index = [(coord_to_name[place_list_coord[dist[0]]], dist[1]) for dist in place_distance_index]
	# # print place_distance_index[:5]
	# #retain only the place names from this list
	# place_name_list = zip(*place_distance_index)[0]
	# # print len(place_list)
	# # print place_distance_decrease
	# # print place_distance_decrease
	# # print place_name_list[:5]
	# return place_name_list


# def get_next_place(state, action):

# 	# get list of places for the action
# 	list_places = place_for_action[action]

# 	# from the list of places, get the best possible place
# 	best_place = get_best_place(state, list_places)

# 	return best_place

# assign location coordinates to place names
# get_loc_coordinate()

# list to hold the predicted places for each state
# place_predict = {
	
# 	1: list(),
# 	2: list(),
# 	3: list(),
# 	4: list(),
# 	5: list(),
# 	6: list(),
# 	7: list()
# }

place_predict = {
	
	1: list(),
	2: list(),
	3: list(),
	4: list(),
	5: list(),
	6: list(),
	7: list(),
	8: list(),
	9: list(),
	10: list(),
	11: list(),
	12: list(),
	13: list(),
	14: list(),
	15: list(),
	16: list(),
	17: list(),
	18: list(),
	19: list(),
	20: list(),
}


for i in range(len(states)):

	#get the last place in the state sequence
	# next_place = get_next_place(states[i][-1], policy[i])

	places_from_state = get_best_place_sequence(states[i][-1], policy[i])
	# print places_from_state

	precision_at = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

	for k in precision_at:

		places_from_state_at_k = places_from_state[:k]

		for place in places_from_state_at_k:

			if (states[i][-1], place) not in place_predict[k]:
				place_predict[k].append((states[i][-1], place))


for k in place_predict:
	#get all the predictions at k
	predictions = place_predict[k]
	print len(predictions)
	pickle.dump(predictions, open("tt" + "/history_2/precision_" + str(k) +"/place_predict.p", "wb"))

# 	print states[i], ",", next_place

# 	# add only those predictions that are distinct from the original place	
# 	# if next_place != states[i]:
# 	# 	place_predict[states[i]] = next_place

# 	if (states[i][-1], next_place) not in place_predict:

# 		place_predict.append((states[i][-1], next_place))

# # remove reptitions
# place_predict = list(set(place_predict))
# print place_predict

# # save the predicted places
# pickle.dump(place_predict, open("tt" + "/history_5" + "/place_predict.p", "wb"))

