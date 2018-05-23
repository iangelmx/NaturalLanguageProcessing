# -*- coding: utf-8 -*-
import nltk
import re
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
from mariamysqlib import *
import math

documentos = doQuery("SELECT cuerpo FROM articulos")
docs = []
b=0
tokens = []
longitudes =[]

for a in documentos:
	docs.append(a[0])
	tokens.append(nltk.word_tokenize(a[0]))
	longitudes.append(len( nltk.word_tokenize(a[0]) ))


probabilidades = []
probs = {}

listaPalabras = ['gobierno', 'empresa', 'banco', 
			'política', 'dinero', 'muerte', 
			'internet', 'droga', 'finanzas']

for palabra in listaPalabras:
	for a in range (0, len(tokens)):
		prob = ((nltk.FreqDist(tokens[a])[palabra]) /( longitudes[a] )) * 100
		probabilidades.append( prob )
		probs[palabra+str(a)] = prob

print(probs)
input(".-.-.-.-.-.-.-.-.")
input()
transaccion=[]

transaccion.append("START TRANSACTION;")
transaccion.append("TRUNCATE probabilidades;")
for palabra in listaPalabras:
	for a in range(1,len(docs)+1):
		transaccion.append("INSERT INTO probabilidades (idDocumento, palabra, probabilidad) VALUES('"+str(a)+"','"+str(palabra)+"','"+str(probs[palabra+str(a-1)])+"')")
transaccion.append("COMMIT;")

doTransaction(transaccion)

# Muchos documentos tienen muchos topicos


