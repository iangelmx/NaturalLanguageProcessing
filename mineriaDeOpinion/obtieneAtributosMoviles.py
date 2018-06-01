#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
from collections import Counter
import numpy
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
from mariamysqlib import *
import os
import subprocess
import string

def compute_ngrams(sequence, n):
	return zip(*[sequence[index:] for index in range(n)])

def get_top_ngrams(corpus, ngram_val=1, limit=5): #Corpus -> texto como cadena
	import operator
	tokens = nltk.word_tokenize(corpus)

	ngrams = compute_ngrams(tokens, ngram_val)
	ngrams_freq_dist = nltk.FreqDist(ngrams)
	sorted_ngrams_fd = sorted(ngrams_freq_dist.item(), 
							key=operator.itemgetter(1), reverse=True)
	sorted_ngrams = sorted_ngrams_fd[0:limit]
	sorted_ngrams = [(' '.join(text), freq) for text, freq in sorted_ngrams]

dirpath = os.getcwd()

pathReviewsMoviles = dirpath+"\\..\\deteccionDeSentimientos\\spanishReviewCorpus\\moviles"

#print(pathReviewsMoviles)

archivos = getListFiles(pathReviewsMoviles)

reviews=selectFilesOfSpecificExtension(archivos,'.txt')

#print(reviews)

cadenaGeneral = ""

for review in reviews:
	cadenaGeneral += leeArchivo(pathReviewsMoviles+"\\"+review)
    
exclude = set(string.punctuation)
exclude.update(['¿', '¡', '"'])

archivoStop = open("stopwords_es.txt", mode="r", encoding="utf-8")
stopWordsEsp = []

cadena=archivoStop.readline()
while cadena!= '':
	cadena=cadena.replace('\n','')
	stopWordsEsp.append(cadena)
	cadena=archivoStop.readline()

cadenaGeneral = cadenaGeneral.strip()
#cadenaGeneral = cadenaGeneral.lower()
stop = stopWordsEsp
cadenaTokens = cadenaGeneral.split()
doc_complete=[cadenaGeneral]
#stop_free = " ".join([i for i in cadenaTokens.lower().split() if i not in stop])
def clean(doc):
	stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
	input(stop_free)
	punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
	return punc_free

doc_clean = [clean(doc).split() for doc in doc_complete]

cadena = ""

for elem in doc_clean:
	for a in elem:
		#input(elem)
		cadena+=a+ " "

archivo = open("..\\Lemmatizacion\\cadenaGeneralReviewsMovilesNormalizada.txt", "w")
#archivo.write(cadenaGeneral)
archivo.write(cadena)
archivo.close()

#subprocess.call("python ..\\Lemmatizacion\\lemmatizeTaggedSentsANGEL.py "+cadenaGeneral, shell=True)

#os.system("..\\Lemmatizacion\\lemmatizeTaggedSentsANGEL.py "+cadenaGeneral)
#print("Lo llamó?")

####SELECT DISTINCT lemmaNoun, count(lemmaNoun) FROM `nounsreviewsmoviles` GROUP BY lemmaNoun ORDER BY `count(lemmaNoun)` DESC