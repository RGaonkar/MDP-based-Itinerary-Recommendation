#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import time
import pickle
import numpy as np
# from joblib import Parallel, delayed  
# import multiprocessing

for split in range(0, 10):
	# reading in the input
	actions = pickle.load(open("cv_"+ str(split) + "/history_1" + "/actions.p", "rb"))
	states = pickle.load(open("cv_"+ str(split) + "/history_1" + "/states.p", "rb"))
	transitions = pickle.load(open("cv_"+ str(split) + "/history_1" + "/transition_prob.p", "rb"))
	rewards = pickle.load(open("cv_"+ str(split) + "/history_1" + "/rewards.p", "rb"))

	#initialization - empty array of size - total number of states
	V1 = np.zeros(len(states), np.float)

	#initialization - empty array of size - total number of states
	V2 = np.zeros(len(states), np.float)

	# initialize with empty string - empty list of size - total number of states
	policy = [''] * len(states)

	# keeping track of the loop iterations
	count = 0.0

	def get_max_action(s1, actions_from_state):

		max_utility = -100  #initializing to a very small value

		max_action = actions[0]   #initialize this to action index 0


		for a in actions_from_state:

			# get all the states that have non-zero probability of being reached from s1 with action a
			states_from_action = [s2 for s2 in range(len(states)) if (states[s1], a, states[s2]) in transitions and transitions[(states[s1], a, states[s2])] > 0.0]

			# remove repetitions of the states
			states_from_action = list(set(states_from_action))

			# get the utility
			utility = rewards[(states[s1], a)] + 0.9*sum([V1[s2]*transitions[states[s1], a, states[s2]] for s2 in states_from_action])

			# print utility

			# check if this is the max possible utility
			if utility > max_utility:

				max_utility = utility

				max_action = a 

		# print max_utility, max_action
		return max_utility, max_action


	def calculate_utility(x):

		actions_from_x = []  #list to store actions from state with index x

		#get state from state index
		current_state = states[x]

		#get all the actions from current_state
		for transition in transitions:

			state_start = transition[0]  #get the start state in the transition

			#found the current state in the transition dictionary
			if current_state == state_start:

				#append the actions from current state to the list
				actions_from_x.append(transition[1])  #transition[1] = action
				
		# remove repetitions of these actions
		actions_from_x = list(set(actions_from_x))

		# from all these actions get the one with the maximum expected utility + reward
		max_utility, max_action = get_max_action(x, actions_from_x) 

		return max_utility, max_action

	prev_diff = 0.0
	curr_diff = 0.0

	# for the very first iteration
	# initialize utilities with the rewards
	if count == 0:

		for s_index in range(len(states)):
			V2[s_index], policy[s_index] = calculate_utility(s_index)
	 
	 	V1, V2 = V2, V1


	while max([abs(V1[i] - V2[i]) for i in range(len(states))]) > 0.001:
		
		# current difference in utilities
		curr_diff = max([abs(V1[i] - V2[i]) for i in range(len(states))])
		print curr_diff
		
		# update utility for each state
		for s_index in range(len(states)):
			V2[s_index], policy[s_index] = calculate_utility(s_index)
	 
	 	V1, V2 = V2, V1

	 	count += 1

		# previous difference is that of the previous iteration
		prev_diff = curr_diff

	print V2
	print policy

	pickle.dump(V2, open("cv_"+ str(split) + "/history_1" + "/utilities.p", "wb"))
	pickle.dump(policy, open("cv_"+ str(split) + "/history_1" + "/policy.p", "wb"))

	