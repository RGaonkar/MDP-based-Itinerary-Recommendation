import sqlite3 
from googleplaces import GooglePlaces, types, lang
import pickle

# placeCategory = pickle.load(open("placeCategoryParis.p", "rb"))

# API_KEY = 'AIzaSyBBaZWRhHJbovOC9h4Z1krKQbZLCHiahTg'

# google_places = GooglePlaces(API_KEY)

conn = sqlite3.connect('/home/rad/berlin1.db')
c = conn.cursor()

# lowercase all the place names
c.execute("SELECT place_name FROM geo_tags")
conn.commit()

data = c.fetchall()
conn.commit()

# remove repetitions
data = list(set(data))

for row in data:

	cur = conn.cursor()
	cur.execute("UPDATE geo_tags SET place_name = ? WHERE place_name = ?", (row[0].lower(), row[0]))
	conn.commit()

conn.close()



