import pickle
import codecs

placeCategory = pickle.load(open("placeCategoryBerlin.p", "rb"))

placeCategoryUnicode = dict()

for key in placeCategory:
	print type(key)
	print key

	if isinstance(key, str):
		placeCategoryUnicode[unicode(key, encoding='utf8', errors='strict')] = placeCategory[key]

	else:

		placeCategoryUnicode[key] = placeCategory[key]

pickle.dump(placeCategoryUnicode, open("placeCategoryBerlin.p", "wb"))