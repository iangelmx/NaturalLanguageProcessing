import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords 
import sys
from sklearn.datasets import fetch_20newsgroups
#from sklearn.model_selection import train_test_split
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn import metrics
from collections import Counter
import numpy
sys.path.insert(0, '../Chapter5')
#sys.path.insert(0, '../Chapter5')
from mariamysqlib import *
from functionsNLP import *

def prepareTextSMS(rutaArchivo, keepUknownMessages = False, lemmatization = False):
	uknownMessages = []
	archivo = open(rutaArchivo, "r")
	#stop = set(stopwords.words('english'))
	if lemmatization == True:
		wordnet_lemmatizer = WordNetLemmatizer()
	mensaje = archivo.readline()

	#tokensGrales = tokenizaFrase(leeArchivo("SMS_Spam_Corpus.txt"), wordPunct=True)
	[tokensGrales, rawText] = getTextTokens("SMS_Spam_Corpus.txt",backTextString=True)
	tokensGrales= set(tokensGrales)

	X = [] #Lista de mensajes lemmatizados
	y = [] #Lista de verificación Si es spam->1 sino 0
	while mensaje != '':
		if mensaje:	
			try:
				if 'spam' in mensaje.split()[-1]:
					mensaje = mensaje.strip()
					mensaje=mensaje[:-6]	#Quitamos el ',spam' del final
					if lemmatization == True:
						fraseTokenizada = tokenizaFrase(mensaje, wordPunct=True)
						mensajeLemmatizado = []
						for token in fraseTokenizada:
							tokenLemmatizado = wordnet_lemmatizer.lemmatize(token, pos='v')
							mensajeLemmatizado.append(tokenLemmatizado)
					y.append(1)
					#print("SPAM "+str(mensajeLemmatizado)+"\n")
				elif 'ham' in mensaje.split()[-1]:
					mensaje = mensaje.strip()
					mensaje=mensaje[:-5]
					if lemmatization == True:
						fraseTokenizada = tokenizaFrase(mensaje, wordPunct=True)
						mensajeLemmatizado = []
						for token in fraseTokenizada:
							tokenLemmatizado = wordnet_lemmatizer.lemmatize(token, pos='v')
							mensajeLemmatizado.append(tokenLemmatizado)
					y.append(0)
					#print("HAM"+str(mensajeLemmatizado)+"\n")
				else:
					print("Mensaje con contenido desconocido... ->"+str(mensaje.split()[-1])+ "<-")
					uknownMessages.append(mensaje)

				if lemmatization == True:
					X.append(mensajeLemmatizado)
				X.append(mensaje)
			except Exception as ex:
				print(ex)
		mensaje = archivo.readline()

	if keepUknownMessages == False:
		return [X, y]
	else:
		return [X, y, uknownMessages]


[X, y] = prepareTextSMS("SMS_Spam_Corpus.txt", lemmatization = False)


vector = CountVectorizer()
X_counts = vector.fit_transform(X)

"""vector.fit(mensajesLemmatizadosStrings)

print(vector.vocabulary_)
bolsa = vector.transform(mensajesLemmatizadosStrings)
print("Tamaño Bag of Words -> "+str(bolsa.shape))
print(bolsa.toarray())
"""

tfIdfTransformador = TfidfTransformer()
X_tfidf = tfIdfTransformador.fit_transform(X_counts)

X=X_tfidf
#X=X_counts
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)


#clf = MultinomialNB()
#clf = LogisticRegression()
#clf = KNeighborsClassifier()
clf = LinearSVC()
clf = SVC(kernel='linear')

clf.fit(X_train,y_train)
pred = clf.predict(X_test)

print("-------------")
print("Y_test (verdadera): \n", y_test, '\n')
print("prediction: \n", pred, '\n')
print("Exactitud de predicción: \n", metrics.accuracy_score(y_test, pred), '\n')
print("Matriz de confusión: \n", metrics.confusion_matrix(y_test, pred), '\n')
print("Classification report: \n", metrics.classification_report(y_test, pred))
