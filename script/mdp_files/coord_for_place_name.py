import sqlite3 
import random
import pickle

name_to_coord = {}   #for each place name have a list of location coordinates
coord_to_name = {}   #for each coordinate have a place name

conn = sqlite3.connect("/home/rad/munich2.db")
c = conn.cursor()

	
# def get_loc_coordinate():

	# global name_to_coord

	# c = conn.cursor()
	
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

# #from list of coordinates for each place name, just choose one randomly from the list and update the dictionary in place

# for name in name_to_coord:

# 	place_list = name_to_coord[name]

# 	print place_list

# 	name_to_coord[name] = random.choice(place_list)


print name_to_coord

pickle.dump(name_to_coord, open("name_to_coord.p", "wb"))
pickle.dump(coord_to_name, open("coord_to_name.p", "wb"))


conn.close()