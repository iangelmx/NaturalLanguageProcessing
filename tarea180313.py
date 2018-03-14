import nltk
from nltk.corpus import swadesh
from nltk.corpus import wordnet as wordNet

names = nltk.corpus.names

names.fileids()

def traductor(palabra):
	try:
		en2es = swadesh.entries(['en', 'es'])
		translate = dict(en2es)
		traduccion=translate[palabra]
		return traduccion
	except:
		return "Traducción no disponible para: "+str(palabra)


female_names = names.words('female.txt')
#print(female_names)

cfd = nltk.ConditionalFreqDist(
	(fileid, name[-1])
	for fileid in names.fileids()
	for name in names.words(fileid))
#cfd.plot()
print(wordNet.synsets('motorcar'))
print(wordNet.synset('car.n.01').lemma_names())
print(wordNet.synset('car.n.01').definition())

print("\nIDIOMAS: "+str(wordNet.langs())+"\n")

print(wordNet.synsets('jugar', lang='spa'))

vero = wordNet.synsets('jugar', lang='spa')

for palabras in vero:
	for palabra in palabras.lemma_names():
		print("Palabra-> "+str(traductor(palabra))+ "\t")



a=wordNet.synsets('car')
for synset in a:
	print( synset.lemma_names())
