# remove photos from geo_data that are not present in geo_tags
import sqlite3

conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()

# get location points from geo_tags
c.execute("SELECT latitude, longitude FROM geo_tags")
conn.commit()

geo_tags = c.fetchall()
conn.commit()

geo_tags = list(set(geo_tags))

# get location points from geo_data
c.execute("SELECT latitude, longitude FROM geo_data")
conn.commit()

geo_data = c.fetchall()
conn.commit()

geo_data = list(set(geo_data))

for loc in geo_data:

	#if this location not present in the geo_tags table	
	if loc not in geo_tags:

		print loc

		cur = conn.cursor()
		#remove from the all_data_geo table
		cur.execute("DELETE FROM all_data_geo WHERE latitude = ? AND longitude = ?", (loc[0], loc[1]))
		conn.commit()

conn.close()

