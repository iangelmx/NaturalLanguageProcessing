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
from mariamysqlib import *

def grabaEnBD(table, lista, update=False):
	if update == False:
		transaccion="START TRANSACTION;\n "
		for item in lista:
			transaccion+="INSERT INTO "+table+"(token) VALUES ('"+str(item)+"');\n "
		transaccion+="COMMIT;"
		print("Terminó de armar la transacción INSERT para "+table)
		doQuery(transaccion)
		print("Se culminó transacción en "+table)
	else:
		transaccion="START TRANSACTION;\n"
		#transaction(table, lista)
		index=1
		for item in lista:
			transaccion+="UPDATE `"+table+"` SET token='"+str(item)+"' WHERE `"+table+"`.`id`="+str(index)+";\n "
			index+=1
		transaccion+="COMMIT;"
		print("Terminó de armar la transacción UPDATE para "+table)
		doQuery(transaccion)
		print("Se culminó transacción en "+table)


def guardaEnArchivo(rutaArchivo,lista, renglones=True):
	archivo = open(rutaArchivo, "w")
	archivo.write("Longitud lista: "+str(len(lista))+"\n")
	for elemento in lista:
		archivo.write(elemento+"\n")
	archivo.close()
	print("Se ha guardado en archivo: "+rutaArchivo)

def lemmatizerBD(rutaArchivoLemmas, tokens, tabla, saveToTable=False): #Tabla es a donde se grabarán los tokens y a donde se lemmatizará
	if saveToTable == True:
		grabaEnBD(tabla, tokens, update=False)
	recoverFromDB = doQuery("SELECT token FROM "+tabla+" ORDER BY id;")
	if recoverFromDB:
		tokens=[]
		for elemento in recoverFromDB:
			tokens.append(elemento[0])
	lemmas = open(rutaArchivoLemmas, mode="r", encoding="utf-8")
	cadena=lemmas.readline()
	conteo=0
	transaccion="START TRANSACTION;\n"
	while cadena != '':
		try:
			[lemma, palabra]=cadena.split('\n')[0].split('\t')
			if palabra in tokens:
				transaccion+="UPDATE "+tabla+" set token='"+str(lemma)+"' WHERE token='"+str(palabra)+"';"
				#print("UPDATE tokens_lemmas set token='"+str(lemma)+"' WHERE token='"+str(palabra)+"';")
			if conteo % 1000 == 0:
				print("Actualizando Tokens Conteo-> "+str(conteo))
			cadena=lemmas.readline()
			conteo+=1
		except Exception as ex:
			print(ex)
			pass
	transaccion+="COMMIT;"
	doQuery(transaccion)
	print("Terminó lemmatizing")
	recoverFromDB = doQuery("SELECT token FROM "+tabla+" ORDER BY id;")
	if recoverFromDB:
		tokensSinLemas=[]
		for elemento in recoverFromDB:
			tokensSinLemas.append(elemento[0])
	return tokensSinLemas


def lemmatizer(rutaArchivoLemmas, tokens):
	lemmas = open(rutaArchivoLemmas, mode="r", encoding="utf-8")
	cadena=lemmas.readline()
	conteo=0
	inicio = 0
	maximo = 100000

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
					#doQuery("UPDATE tokens_lemmas SET token = '"+lemma+"' WHERE id="++";")
					#print("Estaba así-> "+str(tokens[index]))
					#print("Se reemplazará por: "+str(lemma))
					tokens[tokens.index(palabra)] = lemma
					#print("Ahora está así-> "+str(tokens[index]) + "\t Conteo-> "+str(conteo))
			#tokens = [w.replace(palabra, lemma) for w in tokens]
			conteo+=1
			if conteo % 2000 == 0:
				print("Working hard-> "+str(conteo))
			if conteo > 500000:
				return tokens
		except:
			pass
	return tokens


textoTokenizado=""
recoverFromDB = doQuery("SELECT token FROM tokens_sin_numeros ORDER BY id;")
if recoverFromDB:
	textoTokenizado=[]
	for elemento in recoverFromDB:
		textoTokenizado.append(elemento[0])
	#print(textoTokenizado)
	#input(len(textoTokenizado))

stopwordslist = set(stopwords.words('spanish'))
#guardaEnArchivo("OUT_FILES\VocabularioSinNumeros.txt", textoTokenizado)

if textoTokenizado =="":
	textoTokenizado = getTextTokens(r"C:\\Excelsior\\e960401_txt.txt")
	grabaEnBD('tokens_sin_numeros', textoTokenizado)

textoTokenizadoNoStopWords = [word for word in textoTokenizado if word not in stopwordslist]
print("Tokens sin números ni stopwords-> len(): "+str(len(textoTokenizadoNoStopWords)))
#------------------------------
##grabaEnBD('tokens_sin_stopwords', textoTokenizadoNoStopWords, update=True)
#------------------------------

#guardaEnArchivo("OUT_FILES\VocabularioNoStop.txt", textoTokenizadoNoStopWords)

#------------------------------
#grabaEnBD('tokens_sin_numeros', textoTokenizado)
#------------------------------

print("Tokens set sin números ni stopwords -> set(len()): "+str(len(set(textoTokenizadoNoStopWords))))

tokensStem = []
spanishStemm = SpanishStemmer(ignore_stopwords=False)
for token in textoTokenizado:
	#stemming = stemmer.stem(token)
	palabraStem = spanishStemm.stem(token)
	tokensStem.append(palabraStem)

#------------------------------
#grabaEnBD('tokens_stem', tokensStem, update=True)
#------------------------------

#nuevosTokens=lemmatizer("lemmatization-es.txt", textoTokenizado)
nuevosTokensLemmas =lemmatizerBD("lemmatization-es.txt", textoTokenizadoNoStopWords, 'tokens_sin_stopwords_lemmas', saveToTable=True)
tokensLemmasSinStopW = []


input("Checar bd")
#grabaEnBD('tokens_lemmas', nuevosTokens)

#guardaEnArchivo("OUT_FILES\lemmas02.txt", nuevosTokens)

#print(stopWords)



"""stemmer = SnowballStemmer("spanish") # Choose a language


print(spanishStemm.stem("acarreo"))
print(spanishStemm.stem("dejase"))
print(spanishStemm.stem("dejaré"))
print(spanishStemm.stem("animoso"))"""

"""input("Snowball:")
print(stemmer.stem("acarreo")) # Stem a word
print(stemmer.stem("dejase")) # Stem a word
print(stemmer.stem("dejaré")) # Stem a word
print(stemmer.stem("animoso")) # Stem a word
"""




#guardaEnArchivo("OUT_FILES\stems.txt", tokensStem)
