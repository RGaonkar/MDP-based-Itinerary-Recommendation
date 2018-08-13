import sqlite3
import pickle
from googleplaces import GooglePlaces, types, lang
import chardet

# load place categories from stored dicts
API_KEY = 'AIzaSyDWFYTN6C8memEtffjM8MvzyIXVpaZEtbs'


google_places = GooglePlaces(API_KEY)

f1 = open("placeCategoryBerlin.p", "rb")
placeCategory = pickle.load(f1)
f1.close()

conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()

c.execute("SELECT latitude, longitude, place_name FROM geo_tags")
conn.commit()

placesDB = c.fetchall()   #get the place names from munich2 db 
conn.commit()

# remove repetitions
placesDB = list(set(placesDB))
print len(placesDB)

not_in_dict = []   #make a list of places that are not already in the dictionary

for row in placesDB:
	
	lat = row[0]
	lon = row[1]
	place = row[2]

	if (place in placeCategory):
		# do nothing if place already added in the placeCategory dictionary
		pass
		

	else:
		# if place not added in the placeCategory dictionary, add it to the not_in_dict list
		not_in_dict.append((lat, lon, place))

# remove repetitions
not_in_dict = list(set(not_in_dict))
print not_in_dict


for row in not_in_dict:
	# for place not already added to the placeCategory dictionary
	# find place category via google places
	lat = row[0]
	lon = row[1]
	place = row[2]
	
	# empty string to hold the place type of the place name
	placeType = ''

	# query google to get the places nearest to the location coordinate and those having the place names in their string
	# look for places in 2km radius
	query_result = google_places.nearby_search(
		lat_lng={'lat' : lat, 'lng' : lon},
		rankby='prominence', radius=1000, name=place)

	# returns a list of places
	# loop through each of the places
	for pResult in query_result.places:

		# placeName = (pResult.name).encode("utf8").lower()
		pResult.get_details()
		# print pResult

		try:
			placeType = pResult.details["types"]  #get the place type for each of the places
			
			# if the the place type is found
			# add it to the placeType variable

			if placeType != '':

				print "Place category found for this place", place

				# get out of the query loop
				continue

			# if place type not assigned, continue quering
			else:

				print "No place category found for this place", place
		
		except Exception, e:

			# print "No place category available from google for:", pResult
			print e
	# add the place name and the place category to the dictionary
	placeCategory[place] = placeType

	# for each new place entry added to the dictionary
	# save the dictionary
	
	# file pointer
	f2 = open("placeCategoryBerlin.p", "wb")
	pickle.dump(placeCategory, f2)
	f2.close()

conn.close()
