# -*- coding: utf-8 -*-
##from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
from mariamysqlib import *
from bs4 import BeautifulSoup as BSHTML



def getNoticeTitle(renglones):
	a=0
	try:
		while "<h3>" not in renglones[a]:
			a+=1
		encabezado =renglones[a]+" "+renglones[a+2]
		encabezadoBeauti = BSHTML(encabezado, 'lxml')
		return encabezadoBeauti.text
	except Exception as ex:
		print(ex)
	return "Error"

archivo = open("C:\Excelsior\e960401.htm", "r", encoding="utf-8")

html = leeArchivo("C:\Excelsior\e960401.htm")
"""
<font face="ARIAL,HELVETICA" size="-2">  
... JUL 28         </font>"""

input("")

html=html.replace("http://www.excelsior.com.mx/9604/960401/", '')
html=html.replace(".html", "")
html=html.replace("<html>", "")

articulos = html.split("</html>")
textoNotas=[]
idNota=1
for articulo in articulos:
	try:
		renglones = articulo.split("\n")
		a=0
		encabezado = getNoticeTitle(renglones)
		print(encabezado)		
		if "hr" in renglones[8]:
			fecha=renglones[8].replace("<", "").replace("/", "").replace(">", "").replace("hr", "").replace("h5 align=right", ""). replace("h5", "").replace("h4 align=right", "")
		else:
			fecha=renglones[9].replace("<", "").replace("/", "").replace(">", "").replace("hr", "").replace("h5 align=right", ""). replace("h5", "").replace("h4 align=right", "")
		b=9
		while renglones[b][0] == "<":
			b+=1
		texto = "\n".join(renglones[b:-4])
		textoBeauti = BSHTML(texto, 'lxml')
		#print("\nCON BEAUTIFUL \n"+textoBeauti.text)
		insertInDB("articulos", ["titulo", "fecha", "cuerpo"], [encabezado, fecha, textoBeauti.text], trace=False)
	except Exception as exc:
		print("Excepción Fuera-> "+str(exc))

#insertInDB("clientes_por_atender", ["numCelular"], [numero])


#Segmentar en N artículos el archivo e960401.html


#		Calcular la frecuencia(conteo) de cada palabra del vocabulario ordenada por su frecuencia
#OPC:	Si se puede, quitar stopwords
#OBLIG:	Chp 3 NLP with Python pp 93-106