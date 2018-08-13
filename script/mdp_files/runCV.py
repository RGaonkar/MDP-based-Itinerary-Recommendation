'''
From the indices get the data points for the CV split 
'''

import pickle
import os

#change the paths for the diferent cities
# cv_data_splits = pickle.load(open("/home/rad/cv_data_splits.p", "rb"))
# train_data = pickle.load(open("/home/rad/train_data.p", "rb"))

# cv_data_splits = pickle.load(open("/home/rad/paris/cv_data_splits.p", "rb"))
# train_data = pickle.load(open("/home/rad/paris/train_data.p", "rb"))

cv_data_splits = pickle.load(open("/home/rad/london/cv_data_splits.p", "rb"))
train_data = pickle.load(open("/home/rad/london/train_data.p", "rb"))

# cv_result_accuracy = []
# cv_result_precision = []
# cv_result_recall = []
# cv_result_f_measure = []

cv_splits = []

for split in cv_data_splits:

	# convert numpy arrray to list
	train_data_idx = split[0].tolist()
	cv_data_idx = split[1].tolist()

	train_data_points = [train_data[i] for i in train_data_idx]
	# print len(train_data_points)
	cv_data_points = [train_data[i] for i in cv_data_idx]
	# print len(cv_data_points)
	
	# training the system
	# os.system("python data_model_new.py %s" % ' '.join(train_data_points))

	# break


	split_points = [train_data_points, cv_data_points]

	print split_points

	print len(split_points)

	cv_splits.append(split_points)

print len(cv_splits)

# pickle.dump(cv_splits, open("/home/rad/cv_splits.p", "wb"))  #gets saved in the home folder for Munich

pickle.dump(cv_splits, open("/home/rad/london/cv_splits.p", "wb"))  #gets saved in the home folder for Munich







