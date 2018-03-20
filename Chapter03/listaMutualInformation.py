#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functionsNLP

def getJointProbability(palabra1, palabra2, listaOraciones):
	conteoW1=0
	conteoW2=0
	conteoW1W2=0
	N = len(listaOraciones)
	for oracion in listaOraciones:
		if palabra1 in oracion:
			conteoW1+=1
		if palabra2 in oracion:
			conteoW2+=1
		if palabra1 and palabra2 in oracion:
			conteoW1W2+=1
	pXw1 = (conteoW1) / (N)
	pXw2 = (conteoW2) / (N)
	

[tokens, textoCompleto] = getTextTokens(rutaArchivo, backTextString=True)

listaOraciones = separaPorOraciones(textoCompleto)



#Quitar las stopwords

#tokens=tokensSinStopWords
