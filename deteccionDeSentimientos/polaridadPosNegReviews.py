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
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split

dirpath = os.getcwd()
#"C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\deteccionDeSentimientos"
#rutaCorpusPolaridad = "C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\Corpus\\ML-SentiCon"
rutaDiccionario = "C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\Corpus\\SpanishSentimentLexicons"
rutaReviewsCine = "C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\deteccionDeSentimientos\\corpusCriticasCine"

transaccion = getPosNegPolarity(rutaReviewsCine, rutaDiccionario) #, maxReviews=100)
#transaccion = prepareRawText2Classify(dirpath, tipoRawText = "reviewCine", rutaDiccionarioPolaridad=rutaCorpusPolaridad, polaridad=True)
resultado = doTransaction(transaccion) #, traceback=True)

print(resultado)

resul1 = doQuery("SELECT (select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='POSITIVE' AND rank='1'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEGATIVE' AND rank='1'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEUTRAL' AND rank='1') FROM DUAL;")

resul2 = doQuery("SELECT (select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='POSITIVE' AND rank='2'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEGATIVE' AND rank='2'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEUTRAL' AND rank='2') FROM DUAL;")
resul3 = doQuery("SELECT (select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='POSITIVE' AND rank='3'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEGATIVE' AND rank='3'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEUTRAL' AND rank='3') FROM DUAL;")
resul4 = doQuery("SELECT (select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='POSITIVE' AND rank='4'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEGATIVE' AND rank='4'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEUTRAL' AND rank='4') FROM DUAL;")
resul5 = doQuery("SELECT (select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='POSITIVE' AND rank='5'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEGATIVE' AND rank='5'),(select count(polaridad) FROM polaridadposnegreviews WHERE polaridad='NEUTRAL' AND rank='5') FROM DUAL;")


print(resul1)

suma1 = int(resul1[0][0])+int(resul1[0][1])+int(resul1[0][2])
suma2 = int(resul2[0][0])+int(resul2[0][1])+int(resul2[0][2])
suma3 = int(resul3[0][0])+int(resul3[0][1])+int(resul3[0][2])
suma4 = int(resul4[0][0])+int(resul4[0][1])+int(resul4[0][2])
suma5 = int(resul5[0][0])+int(resul5[0][1])+int(resul5[0][2])
print("1| "+str((int(resul1[0][0])/suma1) *100)+" | "+str((int(resul1[0][1])/suma1) *100)+" | "+str((int(resul1[0][2])/suma1) *100))
print("2| "+str((int(resul2[0][0])/suma2) *100)+" | "+str((int(resul2[0][1])/suma2) *100)+" | "+str((int(resul2[0][2])/suma2) *100))
print("3| "+str((int(resul3[0][0])/suma3) *100)+" | "+str((int(resul3[0][1])/suma3) *100)+" | "+str((int(resul3[0][2])/suma3) *100))
print("4| "+str((int(resul4[0][0])/suma4) *100)+" | "+str((int(resul4[0][1])/suma4) *100)+" | "+str((int(resul4[0][2])/suma4) *100))
print("5| "+str((int(resul5[0][0])/suma5) *100)+" | "+str((int(resul5[0][1])/suma5) *100)+" | "+str((int(resul5[0][2])/suma5) *100))

