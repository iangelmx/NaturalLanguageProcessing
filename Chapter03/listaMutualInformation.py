#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
from functionsNLP import *
from mariamysqlib import *
import math
from decimal import *

#Entropía, de una palabra, entre más grande sea, más dificil de predecir.
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
	pXw1 = (conteoW1 + 0.5) / (N+1)
	pXw2 = (conteoW2 + 0.5) / (N+1)
	pXw1w2 = (conteoW1W2 + 0.25) / (N+1)
	return [pXw1, pXw2,pXw1w2]

def getMutualInformationOfGobierno(precision=False):
	MI={}
	a=0

	for palabra in tokens:
		#input(palabra)
		#Probabilidad de que W1 esté en oracion: p_w1_1
		[p_w11, p_w21,p_w11_w21] = getJointProbability('gobierno', palabra, listaOraciones)
		p_w10 = 1- p_w11
		p_w20 = 1- p_w21
		
		p_w10_w21 = p_w21 - p_w11_w21
		#p_w10_w20 = p_w20 - p_w10_w21
		p_w10_w20 = p_w10 - p_w10_w21
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

		if precision == False:
			try:
				for u in range (0, 2):
					for v in range (0, 2):
						#print('w1'+str(u)+'w2'+str(v)+" * log2("+'w1'+str(u)+'w2'+str(v)+" / "+'w1'+str(u)+" * "+'w2'+str(v)+" )")
						MI[palabra] = p['w1'+str(u)+'w2'+str(v)] * (math.log2( (p['w1'+str(u)+'w2'+str(v)])/( (p['w1'+str(u)])*(p['w2'+str(v)]) ) ) )

						#print("MI['"+palabra+"'] = "+str(MI[palabra]))
			except Exception as ex:
				#print(ex)
				pass
		else:
			try:
				for u in range (0, 2):
					for v in range (0, 2):
						#print('w1'+str(u)+'w2'+str(v)+" * log2("+'w1'+str(u)+'w2'+str(v)+" / "+'w1'+str(u)+" * "+'w2'+str(v)+" )")
						#resul = p['w1'+str(u)+'w2'+str(v)] * (math.log2( (p['w1'+str(u)+'w2'+str(v)])/( (p['w1'+str(u)])*(p['w2'+str(v)]) ) ) )
						MI[palabra]= Decimal(p['w1'+str(u)+'w2'+str(v)]) * ( (Decimal((p['w1'+str(u)+'w2'+str(v)])).log10() / Decimal(2).log10()) / (Decimal( ( (p['w1'+str(u)])*(p['w2'+str(v)]) ) ).log10() / Decimal(2).log10()) ) #( math.log2( (p['w1'+str(u)+'w2'+str(v)])/( (p['w1'+str(u)])*(p['w2'+str(v)]) ) ) )
						#print("MI['"+palabra+"'] = "+str(MI[palabra]))
			except Exception as ex:
				#print(ex)
				pass

				
		a+=1
		if a%5000 == 0:
			print("Working Hard. A-> "+str(a))
			if precision == False:
				print(palabra+" : "+str(MI[palabra]))
			else:
				print("MI['"+palabra+"'] = "+str(MI[palabra]))
			

	return MI

#def calculateProbabilityWordsAbscents():
	
rutaArchivo="e960401_txt.txt"
[tokens, textoCompleto] = getTextTokens(rutaArchivo, backTextString=True)

listaOraciones = separaPorOraciones(textoCompleto)

#Palabra base= "gobierno"
precision=False
diccionarioMI=getMutualInformationOfGobierno()
"""
entrada = open("SALIDA.txt", "r")
linea = entrada.readline()
linea = entrada.readline()

MIin={}
a=0
while linea != '':
	[key, value] = linea.split(":")
	key=key.replace(' ','')
	value=value.replace(' ','')
	MIin[key]=value
	linea=entrada.readline()
	a+=1
	if a > 7900:
		print(linea)

input("Lectura finalizada")"""


archivo = open("SALIDA_Precisa_gob.txt", "w")
archivo.write("Gobierno...\n")
transaccion = "START TRANSACTION;\n"

#-----------------------------
listaDictOrdenado = sorted(diccionarioMI.items(), key=operator.itemgetter(1))
for a in range (len(listaDictOrdenado)-1, 0,-1):
	transaccion+="INSERT into MutualInformationCad (token, valor) VALUES('"+str(listaDictOrdenado[a][0])+"', '"+str(listaDictOrdenado[a][1])+"');\n"
	archivo.write(str(listaDictOrdenado[a][0])+"\t:\t"+str(listaDictOrdenado[a][1])+"\n" )
	#archivo.write(elemento+" : "+str(MI[elemento])+"\n")
archivo.close()
#-----------------------------

"""
for elemento in diccionarioMI:
	#transaccion+="INSERT into MutualInformation (token, valor) VALUES('"+elemento+"', "+str(diccionarioMI[elemento])+"); \n"	
	archivo.write(elemento+" : "+str(diccionarioMI[elemento])+"\n")"""
transaccion +="COMMIT;\n"
transaccion += "//"

#print(transaccion)
#archivo.close()

print(doQuery(transaccion))
print("Proceso finalizado")




#Quitar las stopwords

#tokens=tokensSinStopWords
