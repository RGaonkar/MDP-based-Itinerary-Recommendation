# script to check if all place names mentioned in the database have place categories assigned to them
import pickle

placeCategory = pickle.load(open("placeCategoryBerlin.p", "rb"))
len(placeCategory.keys())

import sqlite3 
conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()
c.execute("SELECT place_name FROM geo_tags")
data = c.fetchall()
conn.commit()
len(list(set(data)))

data = list(set(data))

for point in data:
	place = point[0]
	
	if (place in placeCategory.keys()):
		pass
		# print place, placeCategory[place]

	else:
		print place, "No dict entry for this place name"

conn.close()
