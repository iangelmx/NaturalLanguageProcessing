import nltk
import re
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
from mariamysqlib import *

[tokens, texto]=getTextTokens("e960401_txt.txt",backTextString=True)	#Una manera que se me ocurrió de tokenizar. Es precisa en un 96.35%

conteo=0
transaccion=[]
transaccion.append("START TRANSACTION;")
for token in tokens:
	lista = re.findall(r'ada$', token)
	if lista:
		conteo+=1
	cadena="INSERT into token_con_stop(token) VALUES('"+str(token)+"');"
	transaccion.append(cadena)
transaccion.append("COMMIT;")
print("Conteo= "+str(conteo))

#abc$	Matches some pattern abc at the end of a string
doTransaction(transaccion)



#Contar cuántas veces se usan palabras que terminan con "ada"
