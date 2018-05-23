# -*- coding: utf-8 -*-
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
from mariamysqlib import *
from nltk.corpus import stopwords
import nltk
import operator

[tokens, abc]=getTextTokens("e960401_txt.txt", backTextString=True)

stopwordslist = set(stopwords.words('spanish'))
#guardaEnArchivo("OUT_FILES\VocabularioSinNumeros.txt", textoTokenizado)
tokensNoStopWords = [word for word in tokens if word not in stopwordslist]

listaTokensFreq = []
ocurrencias = nltk.FreqDist(tokens)


tokensNoRepetidosNoStopWords = set(tokensNoStopWords)

input("Longitud sin repeticiones-> "+str(len(tokensNoRepetidosNoStopWords)))

for token in tokensNoRepetidosNoStopWords:
	diccionario = {token : ocurrencias[token]}
	listaTokensFreq.append(diccionario)

archivo=open("FREQDIST.txt", "w")
ocurrenciasOrdenadas = sorted(ocurrencias.items(), key=operator.itemgetter(1))
for elem in ocurrenciasOrdenadas:
	archivo.write(str(elem)+"\n")
archivo.close()


transaccion = []
transaccion.append("START TRANSACTION;")
for token in listaTokensFreq:
	transaccion.append("INSERT INTO tokens_sin_stopwords (token, ocurrencias) VALUES('"+str([*token][0])+"', "+str(token[[*token][0]])+");")
transaccion.append("COMMIT;")
print("Result-> "+str(doTransaction(transaccion)))
