import sqlite3

def clean_text(text):

	""" Static variables """

	stopword1 = [line.decode('utf8').strip() for line in open("../googlePlaces/irrelevantwords.txt")]    #gather the irrelevant tags

	stopword_english = [line.decode('utf8').strip() for line in open("../googlePlaces/english.txt")]     #the standard english stopwords

	stopword_german = [line.decode('utf8').strip() for line in open("../googlePlaces/german_stopwords.txt")]  

	stopword_spanish = [line.decode('utf8').strip() for line in open("../googlePlaces/spanish_stopwords.txt")]  

	stopword_french = [line.decode('utf8').strip() for line in open("../googlePlaces/french_stopwords.txt")]     #list of german stopwords except the ones with the umlauts

	words_flickr = [line.decode('utf8').strip() for line in open("../googlePlaces/flickrirrelevant.txt")]       #irrelvant tags in flickr

	words_city = [line.decode('utf8').strip() for line in open("../googlePlaces/irrelevantwords.txt")]       #irrelvant tags in flickr

	stopword_flickr_corpus = stopword1 + stopword_english + stopword_german + stopword_french + stopword_spanish + words_flickr + words_city  #combine the two stopword lists

	def remove_characters():
		"Remove special characters from string"
		not_letters_or_digits = u'!"#%()*+,-./:;<=>?@[\]^_`{|}~' #punctuation marks to be eliminated

		translate_table = dict((ord(char), u'') for char in not_letters_or_digits)

		return text.translate(translate_table)

	def pre_process():
		"""Tokenize, lower case and remove repetitions from the text"""

		tagsLower = tags_rem_chars.lower()

		tagsList = tagsLower.split() #split the string into a list

		tagsUnique = list(set(tagsList))

		return tagsUnique

	def remove_stopwords():
		"""Remove stopwords from the text"""

		tagsNoStopwords = [word for word in tags_processed if word not in stopword_flickr_corpus]
		return tagsNoStopwords

	
	tags_rem_chars = remove_characters()
	tags_processed = pre_process()
	tags_rem_stopwords = remove_stopwords()
	tags_rem_stopwords = list(set(tags_rem_stopwords))   #remove repetitions

	tags_new_string = ' '.join(tags_rem_stopwords)
	
	# print tags_rem_stopwords

	return tags_new_string #returns a list of filtered words

def read_data():

	owner_tags = {}   #dictionary to hold the textual tags for each person

	conn = sqlite3.connect("/home/rad/berlin1.db")
	c = conn.cursor()

	c.execute("SELECT owner_id, title_str, tags_str, description FROM all_data_geo")
	conn.commit()

	data = c.fetchall()
	conn.commit()

	# remove repetitions

	data = list(set(data))

	for row in data:

		rowText = unicode(row[1]) + ' ' + unicode(row[2]) + ' ' + unicode(row[3])

		clean_row_text = clean_text(rowText)

		if clean_row_text:
	
			try:
				owner_tags[row[0].strip()] = owner_tags[row[0].strip()] + ' ' + clean_row_text

			except KeyError, e:				
				owner_tags[row[0].strip()] = clean_row_text


	# print owner_tags
	conn.close()    #close connection to the database

	return owner_tags


def write_data(owner_tags):

	conn = sqlite3.connect("/home/rad/berlin1.db")
	c = conn.cursor()

	for owner in owner_tags:

		c.execute("INSERT OR REPLACE INTO user_pref (owner_id, keywords) VALUES (?, ?)", (owner, owner_tags[owner]))
		conn.commit()

	conn.close()    #close connection to the database

def tokenize(text):
	import nltk

	tokens = nltk.word_tokenize(text)

	return tokens

def tfidf_scores(owner_tags):
	# not using at the moment
	# results not very good
	from sklearn.feature_extraction.text import TfidfVectorizer

	tfidf = TfidfVectorizer(tokenizer=tokenize)

	tfs = tfidf.fit_transform(owner_tags.values())

	tfidf_score_val = {}

	feature_names = tfidf.get_feature_names()

	for owner in owner_tags:

		tags = owner_tags[owner]

		response = tfidf.transform([tags])

		for col in response.nonzero()[1]:

			print feature_names[col], ' - ', response[0, col]
		print "----------------------------------------------------------------------------------------------------------------"

get_owner_tags = read_data()

print get_owner_tags

write_data(get_owner_tags)

# not using this for now. Results not good
# get_keywords = tfidf_scores(get_owner_tags)




