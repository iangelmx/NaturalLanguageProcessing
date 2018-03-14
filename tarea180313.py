#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import swadesh
from nltk.corpus import wordnet as wordNet

# Hipónimo-> Es una relación binaria. Instancia d ela clase 
# Hiperónimo -> Clase

names = nltk.corpus.names

names.fileids()

def traductor(palabra):
	try:
		es2en = swadesh.entries(['es', 'en'])
		translate = dict(es2en)
		traduccion=translate[palabra]
		return traduccion
	except Exception as ex:
		print("Excepción: "+str(ex)+"<-\n")
		return "Traducción no disponible para: "+str(palabra)


palabras=['cenizas', 'nieve', 'hincharse', 'arañar']

"""for palabra in palabras:
	print("Palabra-> "+palabra+" -> "+str(traductor(palabra))+ "\t")"""



"""
for synset in a:
	print( synset.lemma_names())
"""


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

vero = wordNet.synsets('computer')
print(vero)

pc = wordNet.synsets('automobile')
print("PC-> "+str(pc))
tiposComputadora = wordNet.synset('automobile.n.01')


print("hyponyms-> "+str(tiposComputadora.hyponyms()))
print("Hypernyms-> "+str(tiposComputadora.hypernyms()))


print("\n\n Parts (part_meronyms): \n")
partes= tiposComputadora.part_meronyms()

for parte in partes:
	print(str(parte)+", \t")

grupoSemantico= wordNet.synset('bird.n.01').member_holonyms()
print("grupoSemantico"+str(grupoSemantico))


a=wordNet.synsets('car')
for synset in a:
	print( synset.lemma_names())