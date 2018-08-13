#removes all entries from thedatabase that have only one photo per user
import sqlite3

conn = sqlite3.connect('/home/rad/berlin1.db')
c = conn.cursor()

# get the place names for each of the location coordinates
c.execute("SELECT latitude, longitude, place_name FROM geo_tags")
conn.commit()

place_names = c.fetchall()
conn.commit()

# remove repetitions
place_names = list(set(place_names))

# dictionary to hold the place name for each of the location coordinates
loc_place_name = {}

for loc in place_names:
	loc_place_name[(loc[0], loc[1])] = loc[2].strip()

print loc_place_name

# get owner ids
c.execute("SELECT owner_id FROM all_data_geo")
conn.commit()

owners = c.fetchall()
conn.commit()

owners = list(set(owners))

# for each owner get the list of places extracted 
for i in owners:

	c.execute("SELECT latitude, longitude FROM all_data_geo WHERE owner_id = ?", (i[0],))
	conn.commit()

	photos = c.fetchall()
	conn.commit()

	photos_set = list(set(photos))            #remove repeated locations
	print photos_set

	# replace location coordinates with place names 
	photos_set = [loc_place_name[loc] for loc in photos_set if loc in loc_place_name]

	# remove repetitions
	photos_set = list(set(photos_set))

	print photos_set


	# if results in only 2 locations by the owner, delete the owners data 
	
	if(len(photos_set) <= 2):
		
		print "Deleting owner with number of photos ", len(photos_set)
		c.execute("DELETE FROM all_data_geo WHERE owner_id = ?", (i[0],))
		conn.commit()

	print len(photos_set)
	
conn.close()