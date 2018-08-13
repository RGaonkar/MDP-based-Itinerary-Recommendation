from sklearn.cross_validation import train_test_split, KFold

def read_data():
	#read the owner ids from the complete data	
	import sqlite3

	# conn = sqlite3.connect("/home/rad/munich2.db")
	# conn = sqlite3.connect("/home/rad/paris1.db")
	conn = sqlite3.connect("/home/rad/london1.db")

	c = conn.cursor()

	c.execute("SELECT owner_id FROM all_data_geo")
	conn.commit()

	owner_data = c.fetchall()
	conn.commit()

	# remove repetitions
	owner_data = list(set(owner_data))

	# print owner_data

	owners = [owner[0] for owner in owner_data]
	
	# print owners

	return owners

def test_train_split():
	
	split = train_test_split(full_dataset, test_size=0.1, random_state=0)

	train = split[0]
	test = split[1]

	# print len(train)
	# print len(test)

	return train, test

def cross_validation_split():
	
	cv_split = KFold(len(train_data), n_folds=10, shuffle=True)
	cv_split_list = []
	# print len(cv_split)
	# print cv_split
	# cv_split = cv_split.tolist()
	
	for split in cv_split:

		for each_split in split:

			# print each_split
			pass
	
	return cv_split


def write_data():
	import pickle
	# pickle.dump(train_data, open("/home/rad/train_data.p", "wb"))
	# pickle.dump(test_data, open("/home/rad/test_data.p", "wb"))
	# pickle.dump(cv_data_splits, open("/home/rad/cv_data_splits.p", "wb"))

	# pickle.dump(train_data, open("/home/rad/paris/train_data.p", "wb"))
	# pickle.dump(test_data, open("/home/rad/paris/test_data.p", "wb"))
	# pickle.dump(cv_data_splits, open("/home/rad/paris/cv_data_splits.p", "wb"))

	pickle.dump(train_data, open("/home/rad/london/train_data.p", "wb"))
	pickle.dump(test_data, open("/home/rad/london/test_data.p", "wb"))
	pickle.dump(cv_data_splits, open("/home/rad/london/cv_data_splits.p", "wb"))


if __name__ == '__main__':

	full_dataset = read_data()   #get owner ids from the complete dataset
	train_data, test_data = test_train_split() #get the train and test set from the complete data
	print len(train_data), len(test_data) 
	cv_data_splits = cross_validation_split()  #from the train data, get the 10-fold CV splits training data indices
	
	write_data()    #save the data to be used later - in the home folder for munich
