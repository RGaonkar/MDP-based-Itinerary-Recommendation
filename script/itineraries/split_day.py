import sqlite3
import datetime
import time
import itertools
from operator import itemgetter

conn = sqlite3.connect("/home/rad/berlin1.db")

c = conn.cursor()

#def time_diff():
c.execute("SELECT owner_id FROM all_data_geo")
conn.commit()

owners = c.fetchall()
owners = list(set(owners))

for owner in owners:

	c.execute("SELECT photo_id, date_val FROM all_data_geo WHERE owner_id = ? ORDER BY datetime(date_val)", (owner[0],))
	conn.commit()
	photos = c.fetchall()
	photos_new = []
	
	for i in photos:

		p = list(i)   #convert the set to list
		date_object = datetime.datetime.strptime(p[1], "%Y-%m-%d %H:%M:%S").timetuple()
		year = date_object[0]
		month = date_object[1]
		day = date_object[2]
		p[1] = (year, month, day)
		#print year, month, day
		photos_new.append(p)

	#print photos_new

	photos_day = [list(g) for k, g in itertools.groupby(sorted(photos_new, key=itemgetter(1)), itemgetter(1))]
	print photos_day
	print "-------------------------------------------------------------------------------------------------------------------------------------------------------------------"

	if len(photos_day) > 1:     #there is more than one day involved

		for i in range(0, len(photos_day)):

			suffix = str(i)   #denoting the day
			owner_new = owner[0] + '_' + suffix   #add the day number to the owner id
			
			for j in photos_day[i]:    #for all photos in that day , update the owner_id
				
				c.execute("UPDATE all_data_geo SET owner_id = ? WHERE photo_id = ?", (owner_new, j[0])) 
				conn.commit()

conn.close()