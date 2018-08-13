import pickle 
from gensim import corpora, models, similarities
import sqlite3 
import random

NUM_OF_TOPICS = 200

def get_data(tagDoc):

    ID = {} # assign unique ID to the location coordinate or photoID
    tags = [] #list to hold all the location tags in the order of the locID keys
    
    for index, key in enumerate(tagDoc.keys()):
        ID[index] = key
        tags.append(tagDoc[key])
    
    return ID, tags

def train_lsa(data):

	dictionary = corpora.Dictionary(data)

	corpus = [dictionary.doc2bow(text) for text in data]

	tfidf = models.TfidfModel(corpus)

	tfidfData = tfidf[corpus]

	lsi = models.LsiModel(tfidfData, id2word=dictionary, num_topics=NUM_OF_TOPICS)

	lsiData = lsi[tfidfData]

	index = similarities.MatrixSimilarity(lsiData)

	allTopics = lsi.print_topics(NUM_OF_TOPICS)

	# print allTopics

	for topic in allTopics:

		print topic

	return lsi, index, dictionary

def get_sim(text, lsi, index, dictionary):

	vec_bow = dictionary.doc2bow(text)

	vec_lsi = lsi[vec_bow]

	sims = index[vec_lsi]

	simScores = sorted(enumerate(sims), key=lambda item: -item[1])

	getMostSimilarID = simScores[0][0]
	getSimScore = simScores[0][1]

	# getMostSimilarTags = geoDocs[getMostSimilarID]
	# print "Highest similarity score is: ", getSimScore
	# print text
	# print "\n"
	# print getMostSimilarID

	return (getSimScore, getMostSimilarID)


def assign_geo_tags():
	
	loc_tags = pickle.load(open("data/geoDocsLondon.p", "rb"))   # load the geo-tagged data
	photo_tags = pickle.load(open("data/nonGeoDocsLondon.p", "rb"))   # load the non-geo-tagged data

	geo_tagged = get_data(loc_tags)
	non_geo_tagged = get_data(photo_tags)

	geo_ID = geo_tagged[0]
	geo_docs = geo_tagged[1]

	non_geo_ID = non_geo_tagged[0]
	non_geo_docs = non_geo_tagged[1]

	model, trained, dictionary = train_lsa(geo_docs)

	conn = sqlite3.connect("/home/rad/london1.db")
	c = conn.cursor()

	for i, photo_text in enumerate(non_geo_docs):

		photoId = non_geo_ID[i]

		sim_score, sim_ID = get_sim(photo_text, model, trained, dictionary)

		# print sim_score
		# print sim_ID

		if sim_score > 0.8:

			# if photo_text == "world museum architecture germany bayern deutschland bavaria europe bmw munchen muenchen coophimmelblau monachium bmwwelt":

			sim_tags = geo_docs[sim_ID]
			print photo_text
			print sim_tags
			print sim_score
			print
			print"----------------------------------------------------------------------------------------------"
			print
			# # possible_locations = [key for key, value in loc_tags.items() if value == sim_tags]

			# # print possible_locations

			# final_location = geo_ID[sim_ID]

			# print final_location

			# print "-------------------------------------------------------------------------------------------------------------------------------------------------------------"

			# cur = conn.cursor()
			# cur.execute("UPDATE no_to_geo SET latitude = ?, longitude = ? WHERE latitude = '0' AND photo_id = ?", (final_location[0], final_location[1], photoId))
			# conn.commit()

if __name__ == "__main__":

	assign_geo_tags()










    
    
    
    


