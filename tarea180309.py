import nltk
from nltk.corpus import brown
from nltk.corpus import inaugural
from nltk.corpus import udhr
from nltk.corpus import PlaintextCorpusReader
from nltk.text import ConcordanceIndex

def getTextTokens(archivo):	#Una manera que se me ocurrió de tokenizar. Es precisa en un 96.35%
	archivo = open("datos.txt", "w")

	ruta=r"C:\\Excelsior\\e960401_txt.txt"
	#print("ruta->"+str(ruta))
	entrada= open(ruta, mode="r", encoding="utf-8")
	abc=entrada.read()
	abc=abc.lower()

	archivo.write(str(abc))
	archivo.close()
	vocabulario = str(abc)
	#print(type(abc))
	vocabulario = re.findall(r"[\w']+", abc)
	print(vocabulario[:60])
	return [vocabulario, abc]

def unusual_words(text):
	text_vocab = set(w.lower() for w in text if w.isalpha())
	english_vocab = set(w.lower() for w in nltk.corpus.words.words())
	unusual = text_vocab.difference(english_vocab)
	return sorted(unusual)


cdf = nltk.ConditionalFreqDist(
	(genre, word)
	for genre in brown.categories()
	for word in brown.words(categories=genre))



genre_word=[(genre, word)
	for genre in ['news', 'romance']
	for word in brown.words(categories=genre)]

print(len(genre_word))

print(genre_word[:4])
print(genre_word[-4:])

cfd = nltk.ConditionalFreqDist(genre_word)
print(cfd)

cfd = nltk.ConditionalFreqDist(
	(target, fileid[:4])
	for fileid in inaugural.fileids()
	for w in inaugural.words(fileid)
	for target in ['america', 'citizen']
	if w.lower().startswith(target)
	)
cfd = nltk.ConditionalFreqDist(genre_word)
#cfd.tabulate(conditions=['English', 'German_Deutsch'], samples=range(10), cumulative=True)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#cfd.tabulate(conditions=days, samples=range(10), cumulative=True)
cfd.tabulate(samples=days)
cfd.plot(samples=days)

input()

unusual_words()

[vocabulario, textoCompleto] = getTextTokens("eadsf")
print("\n\n")
print(unusual_words(vocabulario))