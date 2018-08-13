#!/usr/bin/env python
from __future__ import division
import sqlite3
from collections import OrderedDict
import pickle
import numpy as np 
from scipy import sparse
import sys

conn = sqlite3.connect("/home/rad/munich2.db")
c = conn.cursor()

# read in the rewards negative value
# f = open('neg_rewards.txt')
# neg_reward = f.readline()
# neg_reward = float(neg_reward.strip())

# PARAMERTERS USED
# input_args = sys.argv[1:]
# print input_args 

#read file with negative reward value
f = open('neg_reward.txt', 'rb')
neg_reward = int(f.readline())  #read the topmost line
f.close()

# neg_reward = -1
print neg_reward

# get the place category dictionary
place_category = pickle.load(open("/home/rad/placeCategoryMunich.p", "rb"))
# print place_category

for split in range(0, 10):

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


	def get_owners():

		c.execute("SELECT owner_id from all_data_geo")
		conn.commit()

		owners = c.fetchall()
		conn.commit()

		owners = list(set(owners))

		# print owners

		return owners

	def get_place_sequence(owners):
		
		train_seq = []    #list to hold place sequences obtained from the training data

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
				train_seq.append(places_unique)     #append these place sequences to train_seq

		# print train_seq
		
		return train_seq

	def get_freq():

		place_seq_freq = {}  #frequency of a pair of places occurring simultaneously
		place_freq = {}  #frequence of a single place occurrence
		
		for place_seq in all_place_sequence:
			
			for i in range(len(place_seq)):

				if i < (len(place_seq) - 1):   
					# print place_seq[i]

					try:
						place_seq_freq[(place_seq[i], place_seq[i+1])] = place_seq_freq[(place_seq[i], place_seq[i+1])] + 1.0
					
					except Exception, e:
						place_seq_freq[(place_seq[i], place_seq[i+1])] = 1.0

				try:
					place_freq[place_seq[i]] = place_freq[place_seq[i]] + 1.0

				except Exception, e:
					place_freq[place_seq[i]] = 1.0 

		return place_seq_freq, place_freq

	def get_place_seq_ratio():

		place_seq_ratio = {}  #dictionary to hold the transition ratio betweeb places given the first place

		for place1, place2 in all_place_seq_freq:
			# round precision to two decimals
			place_seq_ratio[(place1, place2)] = all_place_seq_freq[(place1, place2)] / all_place_freq[(place1)]

		return place_seq_ratio

	def get_action_place_list():

		# get the place category dictionary
		place_category = pickle.load(open("/home/rad/placeCategoryMunich.p", "rb"))
		
		action_places = {}   #dictionary to assign places for each place category

		for place, action_list in place_category.iteritems():

			# only if this place is included in this split of CV
			if place in place_name_split_list:

				for action in action_list:

					try:
						action_places[action].append(place)
					
					except Exception, e:
						action_places[action] = [place]

		return action_places

	def get_transition_prob():

		global transition_prob

		for place1 in all_place_freq:
			
			# for each action from place 1
			for action in action_places_list:
				
				# get list of places for this place category
				places_for_action = action_places_list[action]

				# get intersection
				places_from_place1 = list(set([place2 for place2 in places_for_action if (place1, place2) in all_place_seq_freq]))	

				# places_not_from_place1 = list(set(all_place_freq.keys()) - set(places_from_place1))

				if len(places_from_place1) > 0:

					x = 1.0 / sum([all_place_seq_ratio[place1, place2] for place2 in places_from_place1])

					# print x

					# for places that occur after place1 corresponding to action

					for place2 in places_from_place1:
						transition_prob[(place1, action, place2)] = all_place_seq_ratio[place1, place2] * x
				
				# else:
				# 	print "No transitions from: ", place1
				# 	pass
				# check sum

					# if sum([transition_prob[(place1, action, place2)] for place2 in places_from_place1]) > 1.0:
					# 	print sum([transition_prob[(place1, action, place2)] for place2 in places_from_place1])
					# 	print "Nooooooooo"
	
	def get_rewards():
		# reward defined as the frequency of (s, a) occurring - ratio
		global rewards

		for place1 in all_place_freq:
			
			# get list of places from place1 
			place2_list = [p2 for p1, p2 in all_place_seq_freq if p1 == place1]

			
			#get the reward of taking an action from place1			
			for place2 in place2_list:

				#get place category of place2 
				for each_category in place_category[place2]:
					#reward is the frequency of taking that action (visiting) the place
					try :
						rewards[(place1, each_category)] += float(all_place_seq_freq[(place1, place2)]) / all_place_freq[place1]   

					except:
						rewards[(place1, each_category)] = float(all_place_seq_freq[(place1, place2)]) / all_place_freq[place1]   

				


	# def transition_dict_to_matrix():

	# 	global P

	# 	for i, state1 in enumerate(all_states):
		

	# 		for j, action in enumerate(all_actions):
				

	# 			for k, state2 in enumerate(all_states):

	# 				if (state1, action, state2) in transition_prob:

	# 					P[i, j, k] = transition_prob[(state1, action, state2)]

	# 				else:
	# 					P[i, j, k] = 0.0


	# 	# check if each state has an action assigned
	# 	# for i, state1 in enumerate(all_states):
			
	# 	# 	flag = 0   #when sum is not equal to 1

	# 	# 	for j, action in enumerate(all_actions):

	# 	# 		if sum(P[i, j]) == 1.0:

	# 	# 			flag = 1

	# 	# 	if flag == 0:

	# 	# 		print state1


	# def reward_dict_to_matrix():

	# 	global R

	# 	for i, state in enumerate(all_states):

	# 		for j, action in enumerate(all_actions):

	# 			if (state, action) in rewards:
	# 				R[i, j] = rewards[(state, action)]

	# 			else:
	# 				# add a heavy negative reward
	# 				R[i, j] = neg_reward

	
	place_name_dict, place_name_split_list = get_loc_names()
	
	# get the training data for this split
	all_owners = pickle.load(open("cv_splits.p", "rb"))[split][0]

	#Get training data for test-train evaluation 
	# all_owners = pickle.load(open("train_data.p", "rb"))
	# print all_owners

	all_place_sequence = get_place_sequence(all_owners)

	# print all_place_sequence
	# print all_place_sequence
	all_place_seq_freq, all_place_freq = get_freq()

	# print all_place_seq_freq
	all_place_seq_ratio = get_place_seq_ratio()

	# get the dictionary of action and places list
	action_places_list = get_action_place_list()
	# print action_places_list

	# dictionary to store the transition probability
	transition_prob = {}

	get_transition_prob()

	# dictionary to hold the rewards for each (place, action) pair
	rewards = {}

	get_rewards()

	# get list of all actions
	all_actions = action_places_list.keys()

	# get list of all places
	all_states = all_place_freq.keys()

	# P = np.empty((len(all_states),len(all_actions), len(all_states)))   #matrix to hold the transition probability
	# # convert the transition probability to a matrix
	# transition_dict_to_matrix()

	# R = np.empty((len(all_states), len(all_actions))) #matrix to hold the rewards
	# # convert the reward dictionary to a matrix
	# reward_dict_to_matrix()
	
	# print P
	# save transition dictionary
	pickle.dump(transition_prob, open("cv_" + str(split) + "/history_1" + "/transition_prob.p", "wb"))

	# # save transition probability matrix
	# pickle.dump(P, open("cv_"+ str(split) + "/P.p", "wb"))

	# # print R
	# # save reward matrix
	# pickle.dump(R, open("cv_"+ str(split) + "/R.p", "wb"))

	# save rewards dictionary
	pickle.dump(rewards, open("cv_"+ str(split) + "/history_1" + "/rewards.p", "wb"))

	# print all_actions
	# save actions
	pickle.dump(all_actions, open("cv_"+ str(split) + "/history_1" + "/actions.p", "wb"))

	# print all_states
	# save states
	pickle.dump(all_states, open("cv_"+ str(split) + "/history_1" + "/states.p", "wb"))

	# print action_places_list
	# save places for each action
	pickle.dump(action_places_list, open("cv_"+ str(split) + "/history_1" + "/action_places_list.p", "wb"))
	

conn.close()
