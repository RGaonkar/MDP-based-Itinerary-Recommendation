#!/usr/bin/env python
# from __future__ import division
import sqlite3
from collections import OrderedDict
import pickle


conn = sqlite3.connect("/home/rad/munich2.db")
c = conn.cursor()


for split in range(0, 10):

	#get validation points for each split

	def get_loc_names():

		c.execute("SELECT latitude, longitude, place_name FROM geo_tags")
		conn.commit()

		loc_data = c.fetchall()
		conn.commit()

		place_name = {}   #dictionary to hold place name for each location coordinate

		place_name_list = []     #get all place names that are in this split

		for loc in loc_data:

			place_name[(loc[0], loc[1])] = loc[2]  
			
			if loc[2] not in place_name_list:
				place_name_list.append(loc[2])	
		
		return place_name, place_name_list


	def get_place_sequence(owners):
		
		test_seq = []    #list to hold place sequences obtained from the test data

		for i in owners:

			owner = i

			c.execute("SELECT latitude, longitude FROM all_data_geo WHERE owner_id = ? ORDER BY Datetime(date_val) ASC", (owner,)) #extract places for each owner ordered by the timestamp
			conn.commit()

			places = c.fetchall() #get the locations of the places visited by each user
			conn.commit()                   

			# replace location coordinates with place names
			places_names = [place_name_dict[(p[0], p[1])] for p in places]

			places_unique = list(OrderedDict.fromkeys(places_names))  #remove repetitions while maintaining order

			# print places_unique
			
			
			if len(places_unique) > 2:              #only considering place sequences of greater than 2

				# count = count + 1            #get the number of place sequences that are greater than 2
				# print places_unique
				test_seq.append(places_unique)     #append these place sequences to test_seq

		print len(test_seq)
		
		return test_seq

	def get_test_pairs():

		test_pairs = []

		for each_seq in all_place_sequence:

			for i in range(len(each_seq) - 1):

				test_pairs.append((each_seq[i], each_seq[i+1]))


		# remove reptitions
		test_pairs = list(set(test_pairs))

		return test_pairs

	place_name_dict, place_name_split_list = get_loc_names()
	
	# get the validation data for this split
	all_owners = pickle.load(open("cv_splits.p", "rb"))[split][1]

	# print all_owners

	all_place_sequence = get_place_sequence(all_owners)   #get place sequences corresponding to these owners

	#save the test sequences
	pickle.dump(all_place_sequence, open("cv_" + str(split) + "/test_seq.p", "wb"))

	#get pairs from the test sequences obtained
	test_set_pairs = get_test_pairs()
	# print test_set_pairs

	# save the test points 
	pickle.dump(test_set_pairs, open("cv_" + str(split) + "/test_pairs.p", "wb"))
	
