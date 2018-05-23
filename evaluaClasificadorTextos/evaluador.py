import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
import sys
from collections import Counter
import numpy
sys.path.insert(0, '../Chapter5')
from mariamysqlib import *
#from functionsNLP import *
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *


def printTable():
	cadena = "| Raw Tokens | tokens - stopW | Lemas | Lemma-stopW | Conteo | tf_idf | precision | recall | F-Measure |"
	"""for a in items:
					cadena +="| "+str(a)+"|\t" """
	print(cadena)


def prepareRawText2Classify(rutaArchivo, keepUknownMessages = False, lemmatization = False, tipoRawText = "SMS", quitStopWords = False):
	uknownMessages = []
	archivo = open(rutaArchivo, "r")
	#stop = set(stopwords.words('english'))
	if quitStopWords == True:
		from nltk.corpus import stopwords
		stopWords = set(stopwords.words('english'))
	if lemmatization == True:
		wordnet_lemmatizer = WordNetLemmatizer()
	mensaje = archivo.readline()

	#tokensGrales = tokenizaFrase(leeArchivo("SMS_Spam_Corpus.txt"), wordPunct=True)
	[tokensGrales, rawText] = getTextTokens(rutaArchivo,backTextString=True)
	tokensGrales= set(tokensGrales)

	X = [] #Lista de mensajes lemmatizados
	y = [] #Lista de verificación Si es spam->1 sino 0
	while mensaje != '':
		if mensaje:
			try:
				if tipoRawText == "SMS":
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

	if keepUknownMessages == False:
		return [X, y]
	else:
		return [X, y, uknownMessages]

def evaluaClasificador(X, y, classifier, count=True, tfIdf=False, svcKernel='linear', backAcuracyScore=False, backMatrixConf=False, backClasifRep=False):
	from sklearn.cross_validation import train_test_split
	from sklearn.feature_extraction.text import CountVectorizer
	from sklearn.feature_extraction.text import TfidfTransformer
	from sklearn.linear_model import LogisticRegression
	from sklearn.naive_bayes import MultinomialNB
	from sklearn.neighbors import KNeighborsClassifier
	from sklearn.svm import LinearSVC
	from sklearn.svm import SVC
	from sklearn import metrics
	vector = CountVectorizer()
	X_counts = vector.fit_transform(X)
	if count == True and tfIdf ==False:
		X = X_counts
	else:
		tfIdfTransformador = TfidfTransformer()
		X_tfidf = tfIdfTransformador.fit_transform(X_counts)
		X=X_tfidf

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)
	if classifier == "MultinomialNB":
		clf = MultinomialNB()
	elif classifier == "LogisticReg":
		clf = LogisticRegression()
	elif classifier == "kNN":
		clf = KNeighborsClassifier()
	elif classifier == "LinSVC":
		clf = LinearSVC()
	elif classifier == "SVC":
		clf = SVC(kernel=svcKernel)
	
	clf.fit(X_train,y_train)
	pred = clf.predict(X_test)
	classRep = metrics.classification_report(y_test, pred)
	#print(classRep)
	reporte = classRep.split()
	#input(reporte)
	#precision = reporte[-4]	#TOTAL
	precision = reporte[-11] 	#Class de SPAM
	#recall = reporte[-3]		#TOTAL
	recall = reporte[-10] 		# Clase de SPAM
	fmeasure = reporte[-9] 		#Clase de SPAM
	#input("pres->"+str(precision)+"rec->"+str(recall))
	if backAcuracyScore == False and backMatrixConf == False and backClasifRep == False:
		return [precision, recall, fmeasure]
	elif backAcuracyScore == True and backMatrixConf == False and backClasifRep == False:
		return [precision, recall, fmeasure, metrics.accuracy_score(y_test, pred)]
	elif backAcuracyScore == True and backMatrixConf == True and backClasifRep == False:
		return [precision, recall, fmeasure, metrics.accuracy_score(y_test, pred), metrics.confusion_matrix(y_test, pred)]
	elif backAcuracyScore == True and backMatrixConf == True and backClasifRep == True:
		return [precision, recall, fmeasure, metrics.accuracy_score(y_test, pred), metrics.confusion_matrix(y_test, pred), classRep]

# t, t-stop, lemmas, lemmaStopW, conteo, tfidf, precision, recall, fmeasure

#[X, y] = prepareTextSMS("SMS_Spam_Corpus.txt", lemmatization = False)
######[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True, quitStopWords=True)

svcKernelUser='linear'

#--------------------------------------------------------------------------------------------------------------------------------------------
### EVALUACIÓN Multinomial NB
[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB")
print("\nEvaluación a MultinomialNB\n")
printTable()
print("|     X\t     |                |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB")
print("|      \t     |       X        |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB")
print("|      \t     |                |       |      X      |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB")
print("|      \t     |                |   x   |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#TFIDF MultNB:

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB", tfIdf=True)
print("|     X\t     |                |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB", tfIdf=True)
print("|      \t     |       X        |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB", tfIdf=True)
print("|      \t     |                |       |      X      |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "MultinomialNB", tfIdf=True)
print("|      \t     |                |   x   |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#--------------------------------------------------------------------------------------------------------------------------------------------
### EVALUACIÓN LogisticRegression
[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg")
print("\nEvaluación a Logistic-Regression\n")
printTable()
print("|     X\t     |                |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg")
print("|      \t     |       X        |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg")
print("|      \t     |                |       |      X      |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg")
print("|      \t     |                |   x   |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#TFIDF LogisticRegression:

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg", tfIdf=True)
print("|     X\t     |                |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg", tfIdf=True)
print("|      \t     |       X        |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg", tfIdf=True)
print("|      \t     |                |       |      X      |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LogisticReg", tfIdf=True)
print("|      \t     |                |   x   |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#--------------------------------------------------------------------------------------------------------------------------------------------
### EVALUACIÓN k-Nearest Neighbors
[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN")
print("\nEvaluación a k-Nearest Neighbors\n")
printTable()
print("|     X\t     |                |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN")
print("|      \t     |       X        |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN")
print("|      \t     |                |       |      X      |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN")
print("|      \t     |                |   x   |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#TFIDF k-Nearest Neighbors:

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN", tfIdf=True)
print("|     X\t     |                |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN", tfIdf=True)
print("|      \t     |       X        |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN", tfIdf=True)
print("|      \t     |                |       |      X      |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "kNN", tfIdf=True)
print("|      \t     |                |   x   |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")


#--------------------------------------------------------------------------------------------------------------------------------------------
### EVALUACIÓN LinearSVC
[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC")
print("\nEvaluación a Linear SVC\n")
printTable()
print("|     X\t     |                |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC")
print("|      \t     |       X        |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC")
print("|      \t     |                |       |      X      |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC")
print("|      \t     |                |   x   |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#TFIDF LinearSVC:

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC", tfIdf=True)
print("|     X\t     |                |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC", tfIdf=True)
print("|      \t     |       X        |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC", tfIdf=True)
print("|      \t     |                |       |      X      |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "LinSVC", tfIdf=True)
print("|      \t     |                |   x   |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")


#--------------------------------------------------------------------------------------------------------------------------------------------
### EVALUACIÓN SVC kernel
[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser)
print("\nEvaluación a SVC con kernel="+svcKernelUser+"\n")
printTable()
print("|     X\t     |                |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser)
print("|      \t     |       X        |       |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser)
print("|      \t     |                |       |      X      |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser)
print("|      \t     |                |   x   |             |   X    |        |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

#TFIDF SVC kernel:

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt")
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser, tfIdf=True)
print("|     X\t     |                |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser, tfIdf=True)
print("|      \t     |       X        |       |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True , quitStopWords=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser, tfIdf=True)
print("|      \t     |                |       |      X      |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")

[X, y] = prepareRawText2Classify("SMS_Spam_Corpus.txt", lemmatization=True)
[precision, recall, fmeasure] = evaluaClasificador(X, y, "SVC", svcKernel=svcKernelUser, tfIdf=True)
print("|      \t     |                |   x   |             |        |   X    |    "+precision+"   |  "+recall+"  | "+fmeasure+" |")








#tfIdfTransformador = TfidfTransformer()
#X_tfidf = tfIdfTransformador.fit_transform(X_counts)

#X=X_tfidf
##X=X_counts
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)



##clf = MultinomialNB()
##clf = LogisticRegression()
##clf = KNeighborsClassifier()
#clf = LinearSVC()
##clf = SVC(kernel='linear')

#clf.fit(X_train,y_train)
#pred = clf.predict(X_test)

##print("-------------")
##print("Y_test (verdadera): \n", y_test, '\n')
##print("prediction: \n", pred, '\n')
#print("Exactitud de predicción: \n", metrics.accuracy_score(y_test, pred), '\n')
#print("Matriz de confusión: \n", metrics.confusion_matrix(y_test, pred), '\n')
#print("Classification report: \n", metrics.classification_report(y_test, pred))

#print("\n")

#printTable(lista, "Multinomial NaiveBayes")
