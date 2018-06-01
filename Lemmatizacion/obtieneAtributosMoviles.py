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

dirpath = os.getcwd()

pathReviewsMoviles = dirpath+"\\..\\deteccionDeSentimientos\\spanishReviewCorpus\\moviles"

#print(pathReviewsMoviles)

archivos = getListFiles(pathReviewsMoviles)

reviews=selectFilesOfSpecificExtension(archivos,'.txt')

#print(reviews)

cadenaGeneral = ""

for review in reviews:
	cadenaGeneral += leeArchivo(pathReviewsMoviles+"\\"+review)

cadenaGeneral = cadenaGeneral.strip()

os.system("python lemmatizeTaggedSentsANGEL.py "+cadenaGeneral)
print("Lo llamó?")