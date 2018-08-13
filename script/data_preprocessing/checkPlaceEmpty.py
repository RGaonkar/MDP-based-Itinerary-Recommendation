# Code to check if place is empty
import sqlite3 
conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()

# FIRST_ROW_ID = 2503

c.execute("SELECT rowid, place_name FROM geo_tags WHERE place_name == ?", ('paris',))
conn.commit()

# check length of the data retrieved
data = c.fetchall()
conn.commit()

#Get the row id of the first row
FIRST_ROW_ID = data[0][0]
print "The first row id is:", FIRST_ROW_ID

data = list(set(data))

print len(data)

row_id_list = []   #Store the row ids in a list

for row in data:

	# print row[0] - FIRST_ROW_ID, row[1]

	row_id_list.append(row[0])

#sort the row ids 
row_id_list.sort()

#print the sorted row ids
for row in row_id_list:
	print row
conn.close()