#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa que obtiene los contextos de cada palabra con una ventana de 8
de todas las palabras del archivo e960401.html
"""

from nltk.corpus import PlaintextCorpusReader
from nltk.text import ConcordanceIndex
import nltk.tokenize
import nltk
import re

def imprimeElementoDetallesVocabulario(indice):
	print("\n\nDetalles del vocabulario.\n")

	print("Diccionario Completo No: "+str(indice)+" -> "+str(detallesVocabulario[indice]))

	input("\nPalabra: "+str(detallesVocabulario[indice]['palabra']))
	input("Ocurrencias: "+str(detallesVocabulario[indice]['ocurrencias']))
	print("Contexto Izq-> "+ str( detallesVocabulario[indice]['contextoIzq'] ) )
	print("Contexto Der-> "+ str( detallesVocabulario[indice]['contextoDer'] ) )

def getTextTokens(rutaArchivo, keepNumbers=False, backTextString=False):	#Una manera que se me ocurrió de tokenizar. Es precisa en un 96.35%
	ruta=rutaArchivo
	#print("ruta->"+str(ruta))
	entrada= open(rutaArchivo, mode="r", encoding="utf-8")
	abc=entrada.read()
	abc=abc.lower()
	tokens = nltk.tokenize.word_tokenize(str(abc))
	if keepNumbers == False:
		alphatokens = [word for word in tokens if word.isalpha()]
		tokens=alphatokens				#Libera los tokens de números y símbolos raros
		if backTextString == True:
			return [tokens, abc]
	return tokens

def getContext(vocabTokenizado, contextos=False):	#Con ésta función puedo tokenizar al 100%.
	#Es una imitación de la función .concordance() Aprovéchenla :D
	contextoIzq = []
	contextoDer = []
	ci = ConcordanceIndex(vocabTokenizado)	#Hashea todos los tokens
	palabra = input("\n\nIntroduce la palabra a comparar: ")
	palabra = palabra.replace('\n', '')
	palabra = palabra.lower()
	resultados = concordance(ci, palabra)

	if contextos != False: #Si no se estipula que se desean regresar los contextos, no ejecuta el siguiente bloque y se salta hasta el return resultados
		palAnt=0
		palSig=""

		for renglon in resultados:
			palAnt=0
			renglon = renglon.split()
			for w in renglon:
				w = w.lower()
				if w == palabra:
					break		#El ciclo se rompe cuando la palabra es igual
				palAnt+=1		#El último valor que guardará es la posicion de w
			#print("len(renglon)->"+str(len(renglon)))
			#print("pal->"+str(palAnt))

			contextoIzq.append(renglon[palAnt-1])
			contextoDer.append(renglon[palAnt+1])
		return [contextoIzq, contextoDer, resultados]		#Descomentar si se desea obtener todo el contexto izq y derecho + el resultado.	
	return resultados



def concordance(ci, word, width=75, lines=500):		#Es una versión re-escrita de .concordance() la ocupo para getContext()
    """
    Sobreescritura de: nltk.text.ConcordanceIndex.print_concordance y regresa los valores en lugar de imprimirlos
    Ver más en:
    http://www.nltk.org/api/nltk.html#nltk.text.ConcordanceIndex.print_concordance
    """
    half_width = (width - len(word) - 2) // 2
    context = width // 4 # approx number of words of context

    results = []
    offsets = ci.offsets(word)

    if offsets:
        lines = min(lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join(ci._tokens[i-context:i]))
            right = ' '.join(ci._tokens[i+1:i+context])
            left = left[-half_width:]
            right = right[:half_width]
            results.append('%s %s %s' % (left, ci._tokens[i], right))
            lines -= 1
    return results


def cuentaOcurrenciasEnContexto(palabra, contexto):
	b=0
	conteo={}
	for a in contexto:
		if palabra == a:
			#print(str(palabra)+" -> "+str(a)+" -> "+str(b))
			b=b+1
	conteo[palabra]=str(b)
	return conteo

def unusual_words(text):
	text_vocab = set(w.lower() for w in text if w.isalpha())
	english_vocab = set(w.lower() for w in nltk.corpus.words.words())
	unusual = text_vocab.difference(english_vocab)
	return sorted(unusual)


FreqDistTodas = {}
b=0
corpus_root = r"C:\Excelsior"
"""wordlists = PlaintextCorpusReader(corpus_root, '.*')
wordlists.fileids()
corpusExcelsior = wordlists.words('e960401_txt.txt')
emma = nltk.Text(corpusExcelsior)"""

#print(wordlists.words('e960401_txt.txt')[:50]) 		#Imprime los primeros 50 tokens.
textoTokenizado= getTextTokens(r"C:\\Excelsior\\e960401_txt.txt", keepNumbers=True)

archivo = open("Vocabulario.txt", "w")

for elemento in textoTokenizado:
	archivo.write(elemento+"\n")
archivo.close()

vocabulario = textoTokenizado
file = open("tokens.txt", "w")
for palabra in vocabulario:
	file.write(str(palabra)+"\n")
file.close()
input("Se guardó en archivo")


#concordancias=getContext(textoTokenizado, contextos=False)

detallesVocabulario = []
diccionarioContextos={}

#ventana8
a=0
ocurrencias = nltk.FreqDist(textoTokenizado)

for elemento in vocabulario:
	try:
		if a<5:
			contexIzq = vocabulario[0:a]
		else:
			contexIzq = vocabulario[a-4:a]
		if a>=((len(vocabulario))-4):
			contexDer = vocabulario[a+1:len(vocabulario)]
		else:
			contexDer = vocabulario[a+1:a+5]
		contextosIzqDer = contexIzq + contexDer
	except Exception as ex:
		print(ex)

	diccionario = {'palabra':elemento, 'ocurrencias':ocurrencias[elemento], 'contextoIzq':contexIzq, 'contextoDer':contexDer, 'contextosIzqDer':contextosIzqDer}
	diccionarioContextos[elemento]=diccionario
	detallesVocabulario.append(diccionario)
	a+=1

#print("Longitud del diccionario vocabulario-> "+str(len(detallesVocabulario)))
#imprimeElementoDetallesVocabulario(1)

print("Detalles gobierno->\n"+str(diccionarioContextos['gobierno']))

print("Longitud vocabulario con repeticiones: "+ str(len(vocabulario)))
vocabularioSinRepeticiones = set(vocabulario)
print("Sin repeticiones-> "+str(len(vocabularioSinRepeticiones)))

#detallesVocabulario[0]['vectorPalabras']=[0,1,5,2,3,5]




diccionarioGral = {}
gobiernos = []
conteo=0
ocurrencias=[]
for indice in range(0, len(detallesVocabulario)):
	detallesVocabulario[indice]['vectorPalabras']=[]
	for palabra in vocabularioSinRepeticiones:
		freqs = nltk.FreqDist(detallesVocabulario[indice]['contextosIzqDer'])
		ocurrencias = freqs['gobierno']
		detallesVocabulario[indice]['vectorPalabras'].append(ocurrencias)

	if indice%100 == 0:
		print("Working hard")
	#print("len-> "+str(len(detallesVocabulario[indice]['vectorPalabras'])))

archivo = open("ResultadosConteos.txt", "w")
for elemento in detallesVocabulario:
	archivo.write(str(elemento)+"\n")
archivo.close()

"""
for palabra in vocabularioSinRepeticiones:
	for indice in range(0, len(detallesVocabulario)):
		if detallesVocabulario[indice]['palabra'] == 'gobierno':
			#print(detallesVocabulario[indice])
			freqs = nltk.FreqDist(detallesVocabulario[indice])
			ocurrencias = freqs['gobierno']
			#print("Ocurrencias->" +str(ocurrencias))
			gobiernos.append(ocurrencias)
		if indice%1000 == 0:
			print("Working "+str(indice))
	conteo+=1
	if conteo%1000 == 0:
		print("Working hard "+str(conteo))
	#print("Palabra del vocabulario-> "+str(palabra))
"""
print("Longitud detallesVocabulario[0]['vectorPalabras'] "+str(len(detallesVocabulario[0]['vectorPalabras'])))
print("\n"+str(detallesVocabulario[0]['vectorPalabras']))



"""
#obtener el contexto izquierdo para cada palabra
list(set(contexIzq))
#Tamaño de contexto distinto.
#Encontrar las intersecciones de éstos contextos.
#Y luego ordenar Como un diccionario :v 
El gobierno
El estado
Nuestro estado
Para cada palabra del archivo
"""

#gobierno = (P1, p2, p3, p4, etc..., pn)
#estado = (p1, p2, p3, p4, etc..., pn)
#Luego hacer el producto punto de gobierno con toods los vectores