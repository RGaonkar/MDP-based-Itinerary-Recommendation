#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TO DO : add user preference factor in this

import pickle
import numpy as np
import random
from math import radians, cos, sin, asin, sqrt


for split in range(0, 10):
	# reading in the input
	actions = pickle.load(open("cv_"+ str(split) + "/history_1" + "/actions.p", "rb"))
	states = pickle.load(open("cv_"+ str(split) + "/history_1" + "/states.p", "rb"))
	utility = pickle.load(open("cv_"+ str(split) + "/history_1" + "/utilities.p", "rb"))
	policy = pickle.load(open("cv_"+ str(split) + "/history_1" + "/policy.p", "rb"))
	place_for_action = pickle.load(open("cv_"+ str(split) + "/history_1" + "/action_places_list.p", "rb"))
	name_to_coord = pickle.load(open("name_to_coord.p", "rb"))   #for each place name have a list of location coordinates
	coord_to_name = pickle.load(open("coord_to_name.p", "rb"))
		
	# def get_loc_coordinate():

	# 	global name_to_coord

	# 	import sqlite3
	# 	conn = sqlite3.connect("/home/rad/munich2.db")
	# 	c = conn.cursor()
		
	# 	c.execute("SELECT latitude, longitude, place_name FROM geo_tags")
	# 	conn.commit()

	# 	loc_data = c.fetchall()
	# 	conn.commit()

	# 	# remove repetitions
	# 	loc_data = list(set(loc_data))

	# 	for loc in loc_data:


	# 		try:
	# 			name_to_coord[loc[2]].append((loc[0], loc[1])) 

	# 		except Exception, e:
	# 			name_to_coord[loc[2]] = [(loc[0], loc[1])]

			
	# 		coord_to_name[(loc[0], loc[1])] = loc[2]		
								


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
		start_coord_list = [(float(p[0]), float(p[1])) for p in name_to_coord[start_place]]

		start_coord_list_lat, start_coord_list_lon = zip(*start_coord_list)
		start_coord_avg = (sum(start_coord_list_lat)/len(start_coord_list_lat), sum(start_coord_list_lon)/len(start_coord_list_lon))

		place_list_coord_avg = list()   #list to hold the averaged out coordinates for each of the place names

		for each_place in place_list:
			each_place_coord_list = [(float(p[0]), float(p[1])) for p in name_to_coord[each_place]]
			each_place_coord_list_lat, each_place_coord_list_lon = zip(*each_place_coord_list)
			each_place_coord_avg = (sum(each_place_coord_list_lat)/len(each_place_coord_list_lat), sum(each_place_coord_list_lon)/len(each_place_coord_list_lon))
			place_list_coord_avg.append(each_place_coord_avg)

		# [random.choice(name_to_coord[p]) for p in place_list if p in name_to_coord]

		least_distance = float("inf")
		least_dist_place = ''

		# category_score = 0   #initialize category score to 10

		for i in range(len(place_list_coord_avg)):
			
			current_place = place_list_coord_avg[i]

			distance = euclidean_distance(start_coord_avg, place_list_coord_avg[i])

			if distance < least_distance:

				least_distance = distance

				least_dist_place = place_list[i]

		# print least_dist_place
		return least_dist_place

	def get_next_place(state, action):

		# get list of places for the action
		list_places = place_for_action[action]

		# from the list of places, get the best possible place
		best_place = get_best_place(state, list_places)

		return best_place

	# assign location coordinates to place names
	# get_loc_coordinate()

	# list to hold the predicted places for each state
	place_predict = []

	for i in range(len(states)):

		#get the last place in the state sequence
		print states[i]
		next_place = get_next_place(states[i], policy[i])

		print states[i], ",", next_place

		# add only those predictions that are distinct from the original place	
		# if next_place != states[i]:
		# 	place_predict[states[i]] = next_place

		if (states[i], next_place) not in place_predict:

			place_predict.append((states[i], next_place))

	# remove reptitions
	place_predict = list(set(place_predict))
	print place_predict

	# save the predicted places
	pickle.dump(place_predict, open("cv_"+ str(split) + "/history_1" + "/place_predict.p", "wb"))

	
