import datetime
import sqlite3
conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()

c.execute("SELECT photo_id, date_val FROM all_data_geo")
conn.commit()

list_dates = c.fetchall()

for date in list_dates:

	try:
		date_object = datetime.datetime.strptime(date[1], "%Y-%m-%d %H:%M:%S")
		print date_object

	except Exception, e:
		print e
		c.execute("DELETE FROM all_data_geo WHERE photo_id = ?", (date[0],))
		conn.commit()		

conn.close()