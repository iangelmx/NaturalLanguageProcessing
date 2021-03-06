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

def getPosNegPolarity(rutaCorpusReviews, rutaDiccionario, maxReviews=None):
	import os
	import string
	from bs4 import BeautifulSoup
	
	#path = rutaCorpusReviews + "\\corpusCriticasCine"
	path = rutaCorpusReviews
	#print("Ruta->"+path)
	polaridadReview = 0.0
	exclude = set(string.punctuation)
	exclude.update(['¿', '¡', '"'])
	archivos = getListFiles(path)
	if maxReviews:
		archivosXML = selectFilesOfSpecificExtension(archivos,'xml')[:maxReviews]
		archivosReviewPos = selectFilesOfSpecificExtension(archivos, 'review.pos')[:maxReviews]
	else:
		archivosXML = selectFilesOfSpecificExtension(archivos,'xml')
		archivosReviewPos = selectFilesOfSpecificExtension(archivos, 'review.pos')
	
	#diccionarioPosNegFull = leeArchivo(rutaDiccionario+"\\fullStrengthLexicon.txt", modeReader="utf-8")
	archivoPosNegFull = open(rutaDiccionario+"\\fullStrengthLexicon.txt", mode="r", encoding="utf-8")
	#diccionarioPosNegMedium = leeArchivo(rutaDiccionario+"\\mediumStrengthLexicon.txt", modeReader="utf-8")
	archivoPosNegMedium = open(rutaDiccionario+"\\mediumStrengthLexicon.txt", mode="r", encoding="utf-8")

	diccionarioPosNegFull = archivoPosNegFull.readlines()
	diccionarioPosNegMedium = archivoPosNegMedium.readlines()

	diccionarioPosNegFullPy = {}
	for linea in diccionarioPosNegFull:
		lemma = linea.split()[0]
		polaridad = linea.split()[-1]
		diccionarioPosNegFullPy[lemma] = polaridad
	
	diccionarioPosNegMediumPy = {}
	for linea in diccionarioPosNegMedium:
		lemma = linea.split()[0]
		polaridad = linea.split()[-1]
		diccionarioPosNegMediumPy[lemma] = polaridad

	print("Tamaño de lista de archivos->"+str(len(archivosXML)))

	transaccion = []
	transaccion.append("START TRANSACTION;")
	transaccion.append("TRUNCATE polaridadPosNegReviews;")
	for archivoPos in archivosReviewPos:
		xmlReviewPos = open(path+"\\"+archivoPos, mode="r") #, encoding="utf-8")
		linea = xmlReviewPos.readline()
		polPositive = 0
		polNegative = 0
		while( linea != ''):
			linea = linea.strip()
			try:
				lemma = linea.split()[1]
				if linea.split()[0] not in exclude:
					if lemma in diccionarioPosNegFullPy:
						polaridad = diccionarioPosNegFullPy[lemma]
						if polaridad == "pos":
							polPositive += 1
						elif polaridad == "neg":
							polNegative += 1
					elif lemma in diccionarioPosNegMediumPy:
						polaridad = diccionarioPosNegMediumPy[lemma]
						if polaridad == "pos":
							polPositive += 1
						elif polaridad == "neg":
							polNegative += 1
					elif lemma in diccionarioSentimPolaridadPy and lemma in diccionarioPosNegMediumPy:
						polaridadMedi = diccionarioPosNegMediumPy[lemma]
						polaridadFull = diccionarioPosNegFullPy[lemma]
						if polaridadMedi == polaridadFull and polaridadMedi == "pos":
							polPositive += 1
						elif polaridadMedi == polaridadFull and polaridadMedi == "neg":
							polNegative += 1
						else:
							print("polarMedi->"+polaridadMedi+" polarFull->"+polaridadFull+" lemma->"+lemma)
							pass
			except Exception as ex:
				#print(ex)
				#print(linea + archivoPos)
				pass
			linea = xmlReviewPos.readline()

		if polPositive > polNegative:
			polaridadReview="POSITIVE"
			#print("POS")
		elif polPositive < polNegative:
			polaridadReview="NEGATIVE"
			#print("NEG")
		else:
			polaridadReview = "NEUTRAL"
			#print("NEUTRAL")

		rutaXmlFromPOS = path+"\\"+archivoPos.split('.review.pos')[0]+".xml"
		#input(rutaXmlFromPOS)
		xml = leeArchivo(rutaXmlFromPOS)
		soup = BeautifulSoup(xml, 'lxml')

		metaData = soup.find('review')
		rank = metaData.attrs['rank']

		transaccion.append("INSERT into polaridadPosNegReviews(polaridad, rank, archivoPos, countPositive, countNegative) VALUES('"+str(polaridadReview)+"', '"+str(rank)+"', '"+str(archivoPos)+"', '"+str(polPositive)+"', '"+str(polNegative)+"')")

		
	transaccion.append("COMMIT;")
	
	return transaccion


def prepareRawText2Classify(rutaArchivo, keepUknownMessages = False, lemmatization = False, tipoRawText = "SMS", quitStopWords = False, reviewCategory=None, maxReviews=None, polaridad=False, rutaDiccionarioPolaridad=None):
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
		if polaridad == True:
			polaridadReview = 0.0
		exclude = set(string.punctuation)
		exclude.update(['¿', '¡', '"'])
		archivos = getListFiles(path)
		if maxReviews:
			archivosXML = selectFilesOfSpecificExtension(archivos,'xml')[:maxReviews]
			if polaridad == True:
				archivosReviewPos = selectFilesOfSpecificExtension(archivos, 'review.pos')[:maxReviews]
				diccionarioSentimPolaridadXML = leeArchivo(rutaDiccionarioPolaridad+"\\senticon.es.xml", modeReader="utf-8")

				soup = BeautifulSoup(diccionarioSentimPolaridadXML, 'lxml')

				lemmasDiccionario = soup.findAll('lemma')
				diccionarioSentimPolaridadPy = {}
				for lemmaTag in lemmasDiccionario:
					lemma=str(lemmaTag.get_text().strip())
					polaridadNum = float(lemmaTag.attrs['pol'])
					diccionarioSentimPolaridadPy[lemma] = polaridadNum
					#input("Polaridad->"+str(polaridad)+"<-")
					#input("diccionarioSentimPolaridadPy["+lemma+"] : "+str(polaridad))
				#polaridadesDicc = lemmasDiccionario.attrs['rank']
			#input(archivosXML)
			#input(archivosReviewPos)

		else:
			archivosXML = selectFilesOfSpecificExtension(archivos,'xml')
			if polaridad == True:
				archivosReviewPos = selectFilesOfSpecificExtension(archivos, 'review.pos')
				diccionarioSentimPolaridadXML = leeArchivo(rutaDiccionarioPolaridad+"\\senticon.es.xml", modeReader="utf-8")

				soup = BeautifulSoup(diccionarioSentimPolaridadXML, 'lxml')

				lemmasDiccionario = soup.findAll('lemma')
				diccionarioSentimPolaridadPy = {}
				for lemmaTag in lemmasDiccionario:
					lemma=str(lemmaTag.get_text().strip())
					polaridadNum = float(lemmaTag.attrs['pol'])
					diccionarioSentimPolaridadPy[lemma] = polaridadNum
		#print(archivosXML)
		print("Tamaño de lista de archivos->"+str(len(archivosXML)))
		try:
			if polaridad == True:
				transaccion = []
				transaccion.append("START TRANSACTION;")
				transaccion.append("TRUNCATE polaridadReviews;")
				for archivoPos in archivosReviewPos:
					xmlReviewPos = open(path+"\\"+archivoPos, mode="r") #, encoding="utf-8")
					linea = xmlReviewPos.readline()
					polaridadReview = 0.0
					while( linea != ''):
						linea = linea.strip()
						try:
							lemma = linea.split()[1]
							if linea.split()[0] not in exclude:
								if lemma in diccionarioSentimPolaridadPy:
									polaridadReview+=diccionarioSentimPolaridadPy[lemma]
						except Exception as ex:
							#print(ex)
							#print(linea + archivoPos)
							pass
						linea = xmlReviewPos.readline()

					rutaXmlFromPOS = path+"\\"+archivoPos.split('.review.pos')[0]+".xml"
					#input(rutaXmlFromPOS)
					xml = leeArchivo(rutaXmlFromPOS)
					soup = BeautifulSoup(xml, 'lxml')

					metaData = soup.find('review')
					rank = metaData.attrs['rank']

					transaccion.append("INSERT into polaridadReviews(polaridad, rank, archivoPos) VALUES('"+str(polaridadReview)+"', '"+str(rank)+"', '"+str(archivoPos)+"')")

					
				transaccion.append("COMMIT;")
				
				return transaccion
					#soup = BeautifulSoup(xmlPos, 'lxml')
			for archivo in archivosXML:
				xml = leeArchivo(path+"\\"+archivo)
				soup = BeautifulSoup(xml, 'lxml')

				body = soup.find('body')
				review = body.get_text().strip().lower().replace('\n', ' ')
				review = ''.join(char for char in review if char not in exclude)
				
				metaData = soup.find('review')
				rank = metaData.attrs['rank']
				
				rankNumber = int(rank)
				y.append(rankNumber)
				X.append(review)


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

def leeArchivo(rutaArchivo, modeReader=None):
	if modeReader:
		file = open(rutaArchivo, mode="r",encoding=modeReader ) # encoding="utf-8")
	else:
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

