#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functionsNLP import *
import math

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
	pXw1w2 = (conteoW1W2) / (N)
	return [pXw1, pXw2,pXw1w2]

def getMutualInformationOfGobierno():
	MI={}
	a=0

	for palabra in tokens:
		#input(palabra)
		#Probabilidad de que W1 esté en oracion: p_w1_1
		[p_w11, p_w21,p_w11_w21] = getJointProbability('gobierno', palabra, listaOraciones)
		p_w10 = 1- p_w11
		p_w20 = 1- p_w21
		
		p_w10_w21 = p_w21 - p_w11_w21
		p_w10_w20 = p_w20 - p_w10_w21
		p_w11_w20 = p_w20 - p_w10_w20

		p = {}
		p['w10w20']= p_w10_w20
		p['w10w21']= p_w10_w21
		p['w11w20']= p_w11_w20
		p['w11w21']= p_w11_w21
		p['w10']= p_w10
		p['w11']= p_w11
		p['w20']= p_w20
		p['w21']= p_w21

		try:
			for u in range (0, 2):
				for v in range (0, 2):
					#print('w1'+str(u)+'w2'+str(v)+" * log2("+'w1'+str(u)+'w2'+str(v)+" / "+'w1'+str(u)+" * "+'w2'+str(v)+" )")
					MI[palabra]= p['w1'+str(u)+'w2'+str(v)] * ( math.log2( (p['w1'+str(u)+'w2'+str(v)])/( (p['w1'+str(u)])*(p['w2'+str(v)]) ) ) )
					#print("MI['"+palabra+"'] = "+str(MI[palabra]))
		except Exception as ex:
			#print(ex)
			pass
		a+=1
		if a%5000 == 0:
			print("Working Hard. A-> "+str(a))
			print("MI['"+palabra+"'] = "+str(MI[palabra]))

	return MI

#def calculateProbabilityWordsAbscents():
	
rutaArchivo="e960401_txt.txt"
[tokens, textoCompleto] = getTextTokens(rutaArchivo, backTextString=True)

listaOraciones = separaPorOraciones(textoCompleto)

#Palabra base= "gobierno"

#diccionarioMI=getMutualInformationOfGobierno()



"""
archivo = open("SALIDA.txt", "w")
archivo.write("Gobierno...\n")

for elemento in MI:
	archivo.write(elemento+" : "+str(MI[elemento])+"\n")
archivo.close()

print("Proceso finalizado")
"""





#Quitar las stopwords

#tokens=tokensSinStopWords
