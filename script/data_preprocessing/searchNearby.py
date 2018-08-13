#!/usr/bin/env python
from googleplaces import GooglePlaces, types, lang
import sqlite3
from fuzzywuzzy import fuzz
import re
import pickle
import os

API_KEY = 'AIzaSyCBXTVvr3cUC6aj9jsjAOgs5qiXQ9wDyZ4'

google_places = GooglePlaces(API_KEY)

conn = sqlite3.connect('/home/rad/berlin1.db')
c = conn.cursor()

c.execute("SELECT latitude, longitude, tagString FROM geo_tags WHERE place_name IS null")
conn.commit()

data = c.fetchall()
conn.commit()

print len(data)

# IMP - dictionary to store the place categories
# check if file already exists
if os.path.exists('placeCategoryBerlin.p'):
	# if it does then initialize with the existing dictionary
	placeCategory = pickle.load(open("placeCategoryBerlin.p", "rb"))

else:
	# else initialize a new dictionary
	placeCategory = {}   #dictionary to hold the place category for each place

for loc in data:

	lat = float(loc[0])
	lon = float(loc[1])
	
	text = unicode(loc[2])  #get tags for the corresponding location coordinates

	# print "Row id: ", loc[0]

	query_result = google_places.nearby_search(
		lat_lng={'lat' : lat, 'lng' : lon},
		rankby='prominence', radius=100)

	similarity = 0.0
	bestPlace = ''
	bestPlaceType = ''

	#returns a list of places
	for place in query_result.places:
		#get the place name
		placeName = (place.name).encode("utf8").lower()
		#do fuzzy match with the tag string for that location coordinate
		simNew = fuzz.token_set_ratio(text, placeName)
		
		#find the place with the highest similarity with the tag string
		if simNew > similarity:
			similarity = simNew
			bestPlace = placeName
			# query for place type or category only if it isn't present in the dictionary
			# saving API limit
			if placeName not in placeCategory.keys():
				place.get_details()
				bestPlaceType = place.details[u'types']
			
			else:

				bestPlaceType = placeCategory[placeName]

	#Filter out numbers from the place name string
	bestPlaceFilterNum = re.sub("[0-9]", "", bestPlace)
	
	print bestPlaceFilterNum, ":", similarity, "Place type : ", bestPlaceType
	print "---------------------------------------------------------------------------------------------------------------------------------------------"
	
	if bestPlaceFilterNum != 'berlin':

		if bestPlaceFilterNum not in placeCategory:
			placeCategory[bestPlaceFilterNum] = bestPlaceType

		pickle.dump(placeCategory, open("placeCategoryBerlin.p", "wb"))

		cur = conn.cursor()
		cur.execute("UPDATE geo_tags SET place_name = ? WHERE latitude = ? AND longitude = ?", (unicode(bestPlaceFilterNum, encoding="utf8", errors="replace"), loc[0], loc[1]))
		conn.commit()

	else:
		print "Place found is:", bestPlaceFilterNum

conn.close()

