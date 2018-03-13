#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nltk.corpus import PlaintextCorpusReader
from nltk.text import ConcordanceIndex
import nltk.tokenize
import nltk
import re
from nltk.stem import SnowballStemmer
from functionsNLP import getTextTokens
from nltk.stem.snowball import SpanishStemmer
from nltk.corpus import stopwords

def guardaEnArchivo(rutaArchivo,lista, renglones=True):
	archivo = open(rutaArchivo, "w")
	archivo.write("Longitud lista: "+str(len(lista))+"\n")
	for elemento in lista:
		archivo.write(elemento+"\n")
	archivo.close()
	print("Se ha guardado en archivo: "+rutaArchivo)

def lemmatizer(rutaArchivoLemmas, tokens):
	lemmas = open(rutaArchivoLemmas, mode="r", encoding="utf-8")
	cadena=lemmas.readline()
	conteo=0
	inicio = 200000
	maximo = 30000

	for a in range(0, inicio):
		cadena=lemmas.readline()
		conteo+=1

	while conteo<maximo:
		try:
			cadena=lemmas.readline()
			[lemma, palabra]=cadena.split('\n')[0].split('\t')
			#print([lemma, palabra])
			for token in tokens:
				if palabra == token:
					index=tokens.index(palabra)
					print("Estaba así-> "+str(tokens[index]))
					#print("Se reemplazará por: "+str(lemma))
					tokens[tokens.index(palabra)] = lemma
					print("Ahora está así-> "+str(tokens[index]) + "\t Conteo-> "+str(conteo))
					#print("Lo guardó?\n\n")

			#tokens = [w.replace(palabra, lemma) for w in tokens]
			conteo+=1
			if conteo % 2000 == 0:
				print("Working hard-> "+str(conteo))
			if conteo > 500000:
				return tokens
		except:
			pass
	return tokens

textoTokenizado = getTextTokens(r"C:\\Excelsior\\e960401_txt.txt")
stopwordslist = set(stopwords.words('spanish'))
guardaEnArchivo("OUT_FILES\VocabularioSinNumeros.txt", textoTokenizado)

textoTokenizadoNoStopWords = [word for word in textoTokenizado if word not in stopwordslist]
print("Tokens sin números ni stopwords-> len(): "+str(len(textoTokenizadoNoStopWords)))
guardaEnArchivo("OUT_FILES\VocabularioNoStop.txt", textoTokenizadoNoStopWords)

print("Tokens set sin números ni stopwords -> set(len()): "+str(len(set(textoTokenizadoNoStopWords))))



nuevosTokens=lemmatizer("lemmatization-es.txt", textoTokenizado)

guardaEnArchivo("OUT_FILES\lemmas04.txt", nuevosTokens)


#print(stopWords)
tokensStem = []


stemmer = SnowballStemmer("spanish") # Choose a language
spanishStemm = SpanishStemmer(ignore_stopwords=False)

print(spanishStemm.stem("acarreo"))
print(spanishStemm.stem("dejase"))
print(spanishStemm.stem("dejaré"))
print(spanishStemm.stem("animoso"))

"""input("Snowball:")
print(stemmer.stem("acarreo")) # Stem a word
print(stemmer.stem("dejase")) # Stem a word
print(stemmer.stem("dejaré")) # Stem a word
print(stemmer.stem("animoso")) # Stem a word
"""



for token in textoTokenizado:
	#stemming = stemmer.stem(token)
	palabraStem = spanishStemm.stem(token)
	tokensStem.append(palabraStem)

guardaEnArchivo("OUT_FILES\stems.txt", tokensStem)
