import sqlite3 
from gensim import corpora, models, similarities
import pickle

conn = sqlite3.connect("/home/rad/berlin1.db")
c = conn.cursor()

data = c.execute("SELECT photo_id, title_str, tags_str, description FROM no_to_geo")
conn.commit()

locData = data.fetchall()
conn.commit()

locText = {}    #dictionary to hold the location coordinates
                #corresponding textual meta-data
                
not_letters_or_digits = u'!"#%()*+,-./:;<=>?@[\]^_`{|}~' #punctuation marks to be eliminated

translate_table = dict((ord(char), u'') for char in not_letters_or_digits)

stopword1 = [line.decode('utf8').strip() for line in open("../../../googlePlaces/irrelevantwords.txt")]    #gather the irrelevant tags

stopword_english = [line.decode('utf8').strip() for line in open("../../../googlePlaces/english.txt")]     #the standard english stopwords

stopword_german = [line.decode('utf8').strip() for line in open("../../../googlePlaces/german_stopwords.txt")]  

stopword_spanish = [line.decode('utf8').strip() for line in open("../../../googlePlaces/spanish_stopwords.txt")]  

stopword_french = [line.decode('utf8').strip() for line in open("../../../googlePlaces/french_stopwords.txt")]     #list of german stopwords except the ones with the umlauts

words_flickr = [line.decode('utf8').strip() for line in open("../../../googlePlaces/flickrirrelevant.txt")]       #irrelvant tags in flickr

words_city = [line.decode('utf8').strip() for line in open("../../../googlePlaces/irrelevantwords.txt")]       #irrelvant tags in flickr

stopword_flickr_corpus = stopword1 + stopword_english + stopword_german + stopword_french + stopword_spanish + words_flickr + words_city   #combine the two stopword lists

def translate_non_alphanumerics(to_translate):
    return to_translate.translate(translate_table)


for point in locData:
    
    try:

        text = unicode(point[1]) + ' ' + unicode(point[2]) + ' ' + unicode(point[3])

        text_list = text.split()    #generate a list of tags

        text_lower = [j.lower() for j in text_list]   #lowercase the tags

        text_unique = list(set(text_lower))   #remove repetitions

        text_string = ' '.join(text_unique)

        text_clean = translate_non_alphanumerics(text_string)
        
        text_clean_list = text_clean.split()

        text_filter = []

        # remove stopwords and flickr noise words from tags

        for word in text_clean_list:
        	
        	if word.strip() in stopword_flickr_corpus:
        		pass

        	else:
        		text_filter.append(word.strip())

        text_filter = list(set(text_filter))

        #remove empty strings from the list

        text_filter = [word for word in text_filter if word]

        if len(text_filter) == 0:
        	# print text_filter_flickr
        	continue   #skip the next steps in this loop and move to the next iteration

        try:
        	locText[point[0]] = locText[point[0]] + text_filter
        
        except KeyError, e:
        	locText[point[0]] = text_filter

    except Exception, e:

        print e 
        continue
print locText

pickle.dump(locText, open("data/nonGeoDocsBerlin.p", "wb"))
