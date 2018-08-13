#get the result from our system and that from existing sources
#add all the accurracies to one common file

import csv
import pickle
import sqlite3
import sys
import pandas as pd


# for split in range(0, 10):

precision_at = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# get test data sequences
infile2 = pickle.load(open("tt" + "/test_seq.p", "rb"))
test_set = infile2


for k in precision_at:

	#get the training data results
	print "Results for accuracy @", k
	# print
	infile1 = pickle.load(open("tt" + "/history_2/precision_" + str(k)+"/place_predict.p", "rb"))
	recommendation_result = infile1

	#flatten recommendation list
	recommendation_result_flatten = [item for sublist in recommendation_result for item in sublist]
	recommendation_result_flatten = list(set(recommendation_result_flatten))
	#flatten recommendation list
	test_set_flatten = [item for sublist in test_set for item in sublist]
	test_set_flatten = list(set(test_set_flatten))
	#print recommendation_result_flatten

	#print "--------------------------------------------------------------------------------------------------------------------------------------------------------"
	#print test_set_flatten

	#get the places common in the test and the train set
	common_test_train = set(recommendation_result_flatten).intersection(set(test_set_flatten))
	#print "--------------------------------------------------------------------------------------------------------------------------------------------------------"
	#print common_test_train

	uncommon_test_train = set(test_set_flatten) - common_test_train

	#remove places from paths in test set that are not common to both test and train. Retain the path only if its length > 1
	test_set_new = []

	#remove points from test set that do not correspond to points in the train set
		
	for path in test_set:
		
		new_path = []

		subpaths_in_path = zip(path, path[1:], path[2:])
		# print "Original path:"
		# print path
		# print "Subpaths of this path:"
		# print subpaths_in_path
		# print

		# print "---------------------------------------------------------------------------------------------------------------------------------"		
		
		index = 0
		
		while index < len(subpaths_in_path):

			if subpaths_in_path[index][1] in uncommon_test_train:
				#do not append it to the new path
				# print place  #sanity check
				# print "Subpath to be removed:"
				# print subpaths_in_path[index]
				# print

				index = index + 3

			else:
				#append it to the new path
				if index == (len(subpaths_in_path) - 1):
					new_path += list(subpaths_in_path[index])

				else:
					new_path.append(subpaths_in_path[index][0])

				index = index + 1
		
		# print "Filtered path:"
		# print new_path
		# print "----------------------------------------------------------------------------------------------------------------------------------------------------------"
		if len(new_path) > 1:
			test_set_new.append(new_path)

	# print test_set_new

	# for path in test_set_new:

	# 	print len(path)

	# #----SPLIT DATA INTO PATHS OF DIFFERENT LENGTHS-------------------------------------------------------------------#

	paths_length_n = {}

	for path in test_set_new:

		# print path
		# print 

		for n in range(2, 10):
			################################################
			# print n
			all_paths_length = map(list, zip(*(path[i:] for i in range(n))))
			# print "Paths of length", n
			# print all_paths_length
			# print
			# print "-----------------------------------------------------------------------------------------------------------------------------"
			# print all_paths_length

			for p in all_paths_length:

				# print len(p)
				
				if len(p) > 0:
					if "length" + str(n) not in paths_length_n:
						#initialize a new list
						paths_length_n["length" + str(n)] = [p]

					else:
						paths_length_n["length" + str(n)].append(p)

	# print paths_length_n.keys()

	#save the test paths of different lengths
	pickle.dump(paths_length_n, open("tt" + "/history_2/precision_" + str(k) +"/test_path_seq.p", "wb"))

	#-------------------------------GET ACCURACY OF PATH FOR EACH LENGTH----------------------------------------------------------------------------------------

	#append accuracy of different path lengths to accuracy.csv file
	# ofile = open("tt"+ str(split) + "/accuracy.csv", "a")
	# writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)
	def get_hits(travel_path, path_length):
	#get accuracy for path of length n
		number_of_hits_list = []
		number_of_exact_hits_bool_list = []
		number_of_partial_hits_bool_list = []

		# print len(travel_path)
		
		for each_path in travel_path:

			length_of_path = len(each_path)
			number_of_hits = 0.0     #initialize the number of hits for each path of the test set

			for x in range(length_of_path-1):
				
				subpath_1 = [each_path[x], each_path[x+1]] #(subpath of length1) - i.e. 2 places adjacent to each other

				flag = 0 #initialize o zero, no hit with the recommendation result
				
				for res in recommendation_result:				
					
					if (flag == 1):
						break    #if already found hit for this particular subpath_1, then move to check the next subpath_1
					if ((res[0] == subpath_1[0]) and (res[1] == subpath_1[1])):
						flag = 1   #found a subpath hit
						number_of_hits += 1.0  #increment the number of hits by 1.0

			number_of_hits_list.append(number_of_hits)

			# #add entry to exact hit bool list
			# if (number_of_hits == (length_of_path - 1)):
			# 	number_of_exact_hits_bool_list.append(number_of_hits)

			# else:
			# 	number_of_exact_hits_bool_list.append(0)
			#add entry to exact hit bool list
			if (number_of_hits == (length_of_path - 1)):
				number_of_exact_hits_bool_list.append(1.0)

			# else:
			# 	number_of_exact_hits_bool_list.append(0)
			elif (number_of_hits > 0):
				number_of_partial_hits_bool_list.append(number_of_hits / float(length_of_path - 1))

		# # print number_of_hits_list
		# print number_of_exact_hits_bool_list
		# return sum(number_of_exact_hits_bool_list)

		# print "Exact matches are as follows:"
		# print number_of_exact_hits_bool_list
		# print "Partial matches are as follows:"
		# print number_of_partial_hits_bool_list

		return sum(number_of_exact_hits_bool_list), sum(number_of_partial_hits_bool_list)


	# accuracy = {}   #dict to hold accuracy for different path 
	
	#dict to hold the exact match and partial match accuracies of the different path lengths
	accuracy = {
		"exact" : dict(),
		"partial": dict()
	}

	# accuracy_partial = {} #dict to hold the partial match accuracies of the different path lengths

	for i in range(2, 8):

		if "length" + str(i) in paths_length_n:
			num_of_paths = len(paths_length_n["length" + str(i)])

			# hits = get_hits(paths_length_n["length" + str(i)], i - 1)

			# print "Accuracy of path of length " + str(i-1) + ": "
			# print hits/num_of_paths

			# accuracy["path_length_" + str(i - 1)] = hits/num_of_paths

			hits_exact, hits_partial = get_hits(paths_length_n["length" + str(i)], i - 1)

			# print "Accuracy of path of length " + str(i-1) + ": "
			# print hits/num_of_paths

			# accuracy["path_length_" + str(i - 1)] = hits/num_of_paths

			accuracy["exact"]["path_length_" + str(i - 1)] = hits_exact / float(num_of_paths)
			accuracy["partial"]["path_length_" + str(i - 1)] = hits_partial / float(num_of_paths)


			# print "Exact match accuracy is as follows:"
			# print "Exact match accuracy for path of length", str(i-1), accuracy["exact"]["path_length_" + str(i - 1)]

			# print "Partial match accuracy for path of length", str(i-1), accuracy["partial"]["path_length_" + str(i - 1)]

			# accuracy_exact["path_length_" + str(i-1)] = accuracy_exact_score
			# accuracy_partial["path_length_" + str(i-1)] = accuracy_partial_score

	# print "-----------------------------------------------------------------------------------------------------------------------------------------------------------"
	# print
	accuracy_df = pd.DataFrame.from_dict(accuracy, orient="columns")

	print accuracy_df
	
	print
	# ofile.close()
	#save the dictionary output
	# pickle.dump(accuracy, open("tt" + "/history_5" + "/path_accuracy.p", "wb"))
# break
