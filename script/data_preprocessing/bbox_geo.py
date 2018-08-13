import sqlite3

conn = sqlite3.connect("/home/rad/radhika1/thesis_relevant/newData/dataset_travel_itinerary/berlin1.db")

c = conn.cursor()

c.execute("SELECT photo_id , latitude, longitude FROM geo_data")
conn.commit()

coord = c.fetchall()
conn.commit()

# Bounding-box for Berlin
# ll_lat = 52.33812
# ll_lon = 13.0884
# ur_lat = 52.675499
# ur_lon = 13.76134


for row in coord:

	p_id = row[0]
	
	lat = float(row[1])
	lon = float(row[2])

	#check if the coordinates lie within the bounding box

	if (lat >= ll_lat) and (lat <= ur_lat) and (lon >= ll_lon) and (lon <= ur_lon):
		# print lat
		# print lon
		pass
		#do nothing
		#coordinates = str(lat) + ', ' +str(lon) + '\n'

	else:
		print lat
		print lon
		cur = conn.cursor()		
		cur.execute("DELETE FROM geo_data WHERE photo_id = ?" , (p_id,))
		conn.commit()

conn.close()