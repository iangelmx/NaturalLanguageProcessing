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