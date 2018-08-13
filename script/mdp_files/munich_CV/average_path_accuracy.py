#!/usr/bin/env python
import csv
import pickle
# lists to hold the performance values for all the iterations
accuracy_one = []
accuracy_two = []
accuracy_three = []
accuracy_four = []
accuracy_five = []
accuracy_six = []

for split in range(0, 10):

	# path_accuracy = pickle.load(open("cv_" + str(split) + "/history_1" + "/path_accuracy.p", "rb"))
	path_accuracy = pickle.load(open("bfs/cv_" + str(split) + "/path_accuracy.p", "rb"))


	for key in path_accuracy:

		if key == "path_length_1":

			accuracy_one.append(path_accuracy[key])

		elif key == "path_length_2":

			accuracy_two.append(path_accuracy[key])

		elif key == "path_length_3":

			accuracy_three.append(path_accuracy[key])

		elif key == "path_length_4":

			accuracy_four.append(path_accuracy[key])

		elif key == "path_length_5":

			accuracy_five.append(path_accuracy[key])


		else:

			accuracy_six.append(path_accuracy[key])
	
avg_accuracy_one = sum(accuracy_one)/len(accuracy_one)
avg_accuracy_two = sum(accuracy_two)/len(accuracy_two)
avg_accuracy_three = sum(accuracy_three)/len(accuracy_three)
avg_accuracy_four = sum(accuracy_four)/len(accuracy_four)
avg_accuracy_five = sum(accuracy_five)/len(accuracy_five)
avg_accuracy_six = sum(accuracy_six)/len(accuracy_six)

print "accuracy of length 1", avg_accuracy_one
print "accuracy of length 2", avg_accuracy_two
print "accuracy of length 3", avg_accuracy_three
print "accuracy of length 4", avg_accuracy_four
print "accuracy of length 5", avg_accuracy_five
print "accuracy of length 6", avg_accuracy_six
print
print "------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
print


