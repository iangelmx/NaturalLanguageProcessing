#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Programa que obtiene los contextos de cada palabra con una ventana de 8
de todas las palabras del archivo e960401.html
"""

from nltk.corpus import PlaintextCorpusReader
from nltk.text import ConcordanceIndex
from nltk.tokenize import WordPunctTokenizer
import nltk.tokenize
import nltk
import re
from pickle import dump
from pickle import load

def prepareRawText2Classify(rutaArchivo, keepUknownMessages = False, lemmatization = False, tipoRawText = "SMS", quitStopWords = False, reviewCategory=None, maxReviews=None, polaridad=False):
	uknownMessages = []
	try:
		archivo = open(rutaArchivo, "r")
		[tokensGrales, rawText] = getTextTokens(rutaArchivo,backTextString=True)
		tokensGrales= set(tokensGrales)
		mensaje = archivo.readline()
	except Exception as ex:
		print(ex)
	#stop = set(stopwords.words('english'))
	if quitStopWords == True:
		from nltk.corpus import stopwords
		stopWords = set(stopwords.words('english'))
	if lemmatization == True:
		wordnet_lemmatizer = WordNetLemmatizer()
	
	#tokensGrales = tokenizaFrase(leeArchivo("SMS_Spam_Corpus.txt"), wordPunct=True)
	
	X = [] #Lista de mensajes lemmatizados
	y = [] #Lista de verificación Si es spam->1 sino 0
	if tipoRawText == "SMS":
		while mensaje != '':
			if mensaje:
				try:
					if 'spam' in mensaje.split()[-1]:
						mensaje = mensaje.strip()
						mensaje=mensaje[:-6]	#Quitamos el ',spam' del final
						fraseTokenizada = tokenizaFrase(mensaje, wordPunct=True)
						if lemmatization == True:
							mensajeLemmatizado = []
							for token in fraseTokenizada:
								tokenLemmatizado = wordnet_lemmatizer.lemmatize(token, pos='v')
								mensajeLemmatizado.append(tokenLemmatizado)
						if quitStopWords == True and lemmatization == True:
							mensajeLemmatizado = [ lema for lema in mensajeLemmatizado if lema not in stopWords]
						elif quitStopWords == True and lemmatization == False:
							fraseTokenizada = [token for token in fraseTokenizada if token not in stopWords]
						y.append(1)
						#print("SPAM "+str(mensajeLemmatizado)+"\n")
					elif 'ham' in mensaje.split()[-1]:
						mensaje = mensaje.strip()
						mensaje=mensaje[:-5]
						fraseTokenizada = tokenizaFrase(mensaje, wordPunct=True)
						if lemmatization == True:							
							mensajeLemmatizado = []
							for token in fraseTokenizada:
								tokenLemmatizado = wordnet_lemmatizer.lemmatize(token, pos='v')
								mensajeLemmatizado.append(tokenLemmatizado)
						if quitStopWords == True and lemmatization == True:
							mensajeLemmatizado = [ lema for lema in mensajeLemmatizado if lema not in stopWords]
						elif quitStopWords == True and lemmatization == False:
							fraseTokenizada = [token for token in fraseTokenizada if token not in stopWords]
						y.append(0)
						#print("HAM"+str(mensajeLemmatizado)+"\n")
					else:
						print("Mensaje con contenido desconocido... ->"+str(mensaje.split()[-1])+ "<-")
						uknownMessages.append(mensaje)

					if lemmatization == True and quitStopWords==False:
						X.append(" ".join(mensajeLemmatizado))
					elif lemmatization == True and quitStopWords==True:
						X.append(" ".join(mensajeLemmatizado))
					elif quitStopWords == True and lemmatization==False:
						X.append(" ".join(fraseTokenizada))
					else:
						X.append(mensaje)
				except Exception as ex:
					#print(ex)
					pass
		mensaje = archivo.readline()
	elif tipoRawText == 'review':
		import os
		import string
		if reviewCategory:
			if reviewCategory == 'coches':
				path = rutaArchivo+'\\spanishReviewCorpus\\coches'
			elif reviewCategory == 'hoteles':
				path = rutaArchivo+'\\spanishReviewCorpus\\hoteles'
			elif reviewCategory == 'lavadoras':
				path = rutaArchivo+'\\spanishReviewCorpus\\lavadoras'
			elif reviewCategory == 'libros':
				path = rutaArchivo+'\\spanishReviewCorpus\\libros'
			elif reviewCategory == 'moviles':
				path = rutaArchivo+'\\spanishReviewCorpus\\moviles'
			elif reviewCategory == 'musica':
				path = rutaArchivo+'\\spanishReviewCorpus\\musica'
			elif reviewCategory == 'ordenadores':
				path = rutaArchivo+'\\spanishReviewCorpus\\ordenadores'
			elif reviewCategory == 'peliculas':
				path = rutaArchivo+'\\spanishReviewCorpus\\peliculas'			
				#print(path)
			archivos = getListFiles(path)
			try:
				for archivo in archivos:
					stringFile = leeArchivo(path+"\\"+archivo)
					stringFile = stringFile.strip()
					stringFile = stringFile.lower()
					exclude = set(string.punctuation)
					stringFile = ''.join(char for char in stringFile if char not in exclude)
					if archivo[:2] == 'no':
						#print("Negativo->"+archivo[:2]+"<-")
						y.append(0)
					elif archivo[:3] == 'yes':
						#print("Positivo->"+archivo[:3]+"<-")
						y.append(1)
					X.append(stringFile)
			except Exception as ex:
				print(ex)
	elif tipoRawText == 'reviewCine':
		import os
		import string
		from bs4 import BeautifulSoup
		path = rutaArchivo + "\\corpusCriticasCine"
		#print("Ruta->"+path)
		archivos = getListFiles(path)
		if maxReviews:
			archivosXML = selectFilesOfSpecificExtension(archivos,'xml')[:maxReviews]
			if polaridad == True:
				archivosReviewPos = selectFilesOfSpecificExtension(archivos, 'review.pos')[:maxReviews]
			#input(archivosXML)
			#input(archivosReviewPos)

		else:
			archivosXML = selectFilesOfSpecificExtension(archivos,'xml')
			if polaridad == True:
				archivosReviewPos = selectFilesOfSpecificExtension(archivos, 'review.pos')
		#print(archivosXML)
		print("Tamaño de lista de archivos->"+str(len(archivosXML)))
		try:
			for archivo in archivosXML:
				xml = leeArchivo(path+"\\"+archivo)
				soup = BeautifulSoup(xml, 'lxml')
		
				body = soup.find('body')
				review = body.get_text().strip().lower().replace('\n', ' ')
				
				metaData = soup.find('review')
				rank = metaData.attrs['rank']
				
				exclude = set(string.punctuation)
				exclude.update(['¿', '¡', '"'])
				review = ''.join(char for char in review if char not in exclude)
				
				rankNumber = int(rank)
				y.append(rankNumber)
				X.append(review)
			if polaridad == True:
				for archivoPos in archivosReviewPos:
					xml = leeArchivo(path+"\\"+archivoPos)
					soup = BeautifulSoup
		except Exception as ex:
			print(ex)

	if keepUknownMessages == False:
		return [X, y]
	else:
		return [X, y, uknownMessages]

def getListFiles(path):
	import os
	try:
		archivos = os.listdir(path)
		return archivos
	except Exception as ex:
		print(ex)
		print("Parece que no existen los archivos que se desean obtener")

def selectFilesOfSpecificExtension(archivos,extension):
	selectedFiles = []
	for archivo in archivos:
		if archivo.endswith(extension):
			selectedFiles.append(archivo)
	return selectedFiles

def tokenizaFrase(rawText, wordPunct=False):
	if wordPunct== False:
		fraseTokenizada = nltk.Text(nltk.word_tokenize(rawText))
		return fraseTokenizada
	elif wordPunct==True:
		fraseTokenizada = WordPunctTokenizer().tokenize(rawText)
		return fraseTokenizada
	else:
		return "Tokenización fuera de catálogo"


def tagRawText2POS(listaOraciones):
	existe=False
	unigramEspTagger=None
	try:
		entrada = open('espTagger.pkl', 'rb')
		unigramEspTagger = load(entrada)
		entrada.close()
		existe=True
	except Exception as ex:
		print(ex)

	if unigramEspTagger == None or existe==False:
		print("Generará el archivo")
		patterns = [
		    (r'.*o$', 'NCMS'),               # Sustantivo Masculino
		    (r'.*a$', 'NCFS'),          		 # Sustantivo Femenino
		    (r'.*as$', 'NCFP'),
		    (r'.*os$', 'NCMP')
		]
		regexp_tagger = nltk.RegexpTagger(patterns)
		cess_tagged_sents = nltk.corpus.cess_esp.tagged_sents()

		'''oracion = listaOraciones[10]
		oracionTokenizada = nltk.Text(nltk.word_tokenize(oracion))

		var = regexp_tagger.tag( oracionTokenizada )'''

		""" Training nltk.UnigramTagger usando oraciones desde cess_esp """
		unigramEspTagger = nltk.UnigramTagger( cess_tagged_sents, backoff=nltk.RegexpTagger(patterns))

		archivoTagger = open('espTagger.pkl', 'wb')
		dump(unigramEspTagger, archivoTagger, -1)
		archivoTagger.close()

	print("Etiquetará del archivo pkl")
	listaToken_TAG = []
	for enunciado in listaOraciones:
		oracionTokenizada=nltk.Text(nltk.word_tokenize(enunciado))
		example = unigramEspTagger.tag(oracionTokenizada)
		for item in example:
			listaItem = list(item)
			listaToken_TAG.append(listaItem)
	return listaToken_TAG

def leeArchivo(rutaArchivo):
	file = open(rutaArchivo, "r")
	archivo=file.read()
	file.close()
	return archivo

def separaPorOraciones(cadena):
	sent_tokenizer = nltk.data.load("nltk:tokenizers/punkt/english.pickle")
	listaOraciones=sent_tokenizer.tokenize(cadena)
	return listaOraciones

def imprimeElementoDetallesVocabulario(indice):
	print("\n\nDetalles del vocabulario.\n")
	print("Diccionario Completo No: "+str(indice)+" -> "+str(detallesVocabulario[indice]))
	input("\nPalabra: "+str(detallesVocabulario[indice]['palabra']))
	input("Ocurrencias: "+str(detallesVocabulario[indice]['ocurrencias']))
	print("Contexto Izq-> "+ str( detallesVocabulario[indice]['contextoIzq'] ) )
	print("Contexto Der-> "+ str( detallesVocabulario[indice]['contextoDer'] ) )

def getTextTokens(rutaArchivo, keepNumbers=False, backTextString=False, utf8=False):	#Una manera que se me ocurrió de tokenizar. Es precisa en un 96.35%
	ruta=rutaArchivo
	#print("ruta->"+str(ruta))
	if utf8 == True:
		entrada= open(rutaArchivo, mode="r", encoding="utf-8")
	else:
		entrada= open(rutaArchivo, "r")
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

