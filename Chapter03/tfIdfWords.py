# -*- coding: utf-8 -*-
import nltk
import re
from functionsNLP import *
from mariamysqlib import *
import math

def calculaTF(palabra, vocabTokens):	#Se utiliza conteoPuro de tokens en texto
	ocurrencias = nltk.FreqDist(vocabTokens)
	tf = math.log2(1+ocurrencias[palabra])
	return tf

def calculaIDF(palabra, vocabTokens, textoCompletoStr, smooth=False): #Se usan oraciones como documentos
	listaOraciones = separaPorOraciones(textoCompletoStr)
	M = len(listaOraciones)
	k = 0
	try:
		for oracion in listaOraciones:
			if palabra in oracion:
				k+=1
		if smooth == False:
			idf = math.log2((M+1)/(k))
		elif smooth == True:
			idf = math.log2((M+1+0.5)/(k+1))
		return idf
	except Exception as ex:
		print("Error con: "+palabra+"\n"+str(ex))
		return "ERROR"

listaPalabras = ['gobierno', 'empresa', 'banco', 
				'política', 'dinero', 'muerte', 
				'internet', 'droga', 'finanzas']

"""tokensSinStopBD=doQuery("SELECT token, ocurrencias FROM tokens_sin_stopwords ORDER BY token ASC")
tokensNoStop={}

for elem in tokensSinStopBD:
	tokensNoStop[elem[0]] = elem[1]"""

[tokens, textoStr]= getTextTokens("e960401_txt.txt", backTextString=True)

tfs = {}
idfs = {}

transaccion = []
transaccion.append("START TRANSACTION;")
transaccion.append("TRUNCATE tfs_idfs;")

for palabra in listaPalabras:
	idf = calculaIDF(palabra, tokens,textoStr, smooth=True)
	tf = calculaTF(palabra, tokens)
	try:
		tfIdf=0.0
		tfIdf = (float(tf)*float(idf)) # <----------------- ???
		#transaccion.append("UPDATE tfs_idfs set tf_idf= '"+str(tfIdf)+"' WHERE token = '"+palabra+"';")
		transaccion.append("INSERT INTO tfs_idfs (token, tf, idf, tfIdf) VALUES('"+palabra+"', '"+str(tf)+"', '"+str(idf)+"', '"+str(tfIdf)+"');")
	except Exception as ex:
		transaccion.append("INSERT INTO tfs_idfs (token, tf, idf, tfIdf) VALUES('"+palabra+"', '"+str(tf)+"', '"+str(idf)+"', '"+str(tfIdf)+"');")
		print(ex)

transaccion.append("COMMIT;")

print(doTransaction(transaccion))

