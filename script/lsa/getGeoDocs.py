import sqlite3 
from gensim import corpora, models, similarities
import pickle


conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()

data = c.execute("SELECT latitude, longitude, tagString FROM geo_tags")
conn.commit()

locData = data.fetchall()
conn.commit()

locText = {}    #dictionary to hold the location coordinates
                #corresponding textual meta-data

for point in locData:

    text = unicode(point[2])
    text_list = text.split()

    print text
    try:
    	locText[(point[0], point[1])] = locText[(point[0], point[1])] + text_list
    
    except KeyError, e:
    	locText[(point[0], point[1])] = text_list

pickle.dump(locText, open("data/geoDocsBerlin.p", "wb"))

conn.close()