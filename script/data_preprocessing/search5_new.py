#*/7 * * * * python /home/kma/search2_new.py && tail -n +2 flickr_pages.txt > pages.txt && mv pages.txt flickr_pages.txt
#*/5 * * * * python /home/saumil/search3_new.py && tail -n +2 paris_pg.txt > pages.txt && mv pages.txt paris_pg.txt
#extracting all photos from flickr that are associated with paris

import flickrapi
import sqlite3
import unicodedata
import time


conn = sqlite3.connect("/home/rad/berlin1.db")   #connect to the munich.db

c = conn.cursor()   #creating a cursor object for the database

api_key = u'74c5aba4f6aaf44a76aa336137da00ca'
secret = u'b7aec18d7dd9d9e1'

tags = ['berlin']    #specifying a list of tags to look for
text = 'berlin'   #specifying the text to search for

#get page_number to extract
f = open('berlin_pg.txt')  #opens the text file having the flickr repsonse page numbers . Need this as on one call , flickr returns only one page
page_no = f.readline() #reads the topmost line
page_no.strip() #removes the newline character at the end
f.close() #closes the file

if page_no != '':    #basically to check that the list of page numbers is not exhausted
	
	flickr = flickrapi.FlickrAPI(api_key, secret)  #create a Flickr Api object

	photos = flickr.photos.search(bbox=[13.0884, 52.33812, 13.76134, 52.675499], per_page='100', page_no=page_no, tags=tags, text=text, extras = 'tags, date_taken, description, geo, date_upload')   #call the photos_search method of flickr api with the specified parameters

	#initializing variables
	date_string = ''
	date_upload = ''
	lat = 'noinfo'
	lon = 'noinfo'
	title = ''  #title of the photo

	describe = ''

#going deeper in the lxml tree of the Flickr response

	for child in photos:
		#for every photo_id
		for i in child:

			photo_set = [] #list of all the sets the photo belongs
			#print i.attrib

			tags_string = '' #string consisting of all tags belonging to a photo

			sets = flickr.photos.getAllContexts(api_key = u'74c5aba4f6aaf44a76aa336137da00ca', photo_id = i.attrib["id"]) #using photoid from here get all the sets to which the photo belongs

			#info = flickr.photos_getInfo(photo_id = i.attrib["id"]) #info contains data for title , datetime and tags


			try:
				describe = i.find('description').text    #get description of the photoset associated with the photograph
				print describe

			except Exception, e:
				print e

			try:

				date_string = i.attrib['datetaken']   #get datetaken associated with 
				print date_string
			except Exception, e:
				print e
				
			'''		
			try:
				date_upload = i.attrib['dateupload'] #unix stamp  - get the dateupload attached with the photo		
				print dateupload
			except Exception, e:
				print e
			'''
			try:
				title = i.attrib['title']  #get title for the photo
				print title
			except Exception, e:
				print e


			try:
				tags_string = i.attrib['tags']   #get textual tags associated with the photo
				print tags_string

			except Exception, e:
				print e

			
			for j in sets:
				if j.tag == "set":
					photo_set.append(j.attrib["id"])

			print photo_set
			set_string = ' '.join(photo_set)
			
			#get location information from geotagged photos
			try:
				lat = i.attrib['latitude']
				lon = i.attrib['longitude']

				print lat, lon

			except Exception, e:
				print e				
			
			#insert data into the sqlite database
			c.execute("INSERT OR REPLACE INTO dataset1(photo_id, owner_id, sets_id, date_val, latitude, longitude, title_str, tags_str, description) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)" , (i.attrib["id"], i.attrib["owner"], set_string, date_string, lat, lon, title, tags_string, describe))	
			conn.commit()
			
conn.close()
