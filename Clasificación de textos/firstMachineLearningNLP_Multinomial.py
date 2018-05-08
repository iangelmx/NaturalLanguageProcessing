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
from sklearn import metrics
from collections import Counter
import numpy
sys.path.insert(0, '../Chapter5')
#sys.path.insert(0, '../Chapter5')
from mariamysqlib import *
from functionsNLP import *

def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]    
    all_words = []       
    for mail in emails:    
        with open(mail) as m:
            for i,line in enumerate(m):
                if i == 2:  #Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words
    
    dictionary = Counter(all_words)
    # Paste code for non-word removal here(code snippet is given below) 
    return dictionary

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



#noticias = fetch_20newsgroups(subset='train')
#print("Tipo de dato de noticias.data-> "+str(type(noticias.data)))
#input("Longitud de lineas->"+str(len(X))+" len etiquetas-> "+str(len(y)))


"""mensajesLemmatizadosStrings = []
for lista in X:
	cadena = " ".join(lista)
	#print(cadena)
	mensajesLemmatizadosStrings.append(cadena)
"""
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

#X=X_tfidf
X=X_counts
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)


#clf = MultinomialNB()
clf = LogisticRegression()
#clf = KNeighborsClassifier()

#Si alpha = 1, es Laplace
#Si fit_prior = True, se hace el conteo de palabras en la suma de todas
clf.fit(X_train,y_train)
pred = clf.predict(X_test)

print("-------------")
print("Y_test (verdadera): \n", y_test, '\n')
print("prediction: \n", pred, '\n')
print("Exactitud de predicción: \n", metrics.accuracy_score(y_test, pred), '\n')
print("Matriz de confusión: \n", metrics.confusion_matrix(y_test, pred), '\n')
print("Classification report: \n", metrics.classification_report(y_test, pred))

#bolsa.toarray()
#ocurrenciasDict = nltk.FreqDist(tokensGrales)
#print(ocurrenciasDict)
#valoresOcurrencias=list(ocurrenciasDict.values())
#print("VALORES...")
#print(ocurrenciasDict.values())
#bolsaY = bolsa.toarray()
#print(bolsaY)
#Xe, Xt, ye, yt = train_test_split(bolsa, bolsaY)



#dictionary = Counter(tokensGrales)
#print("Diccionario->"+str(dictionary))



##print(clf.predict(X[2:3]))

"""input(":v:v:v:v")
input()

lr = LogisticRegression()
lr.fit(Xe, ye)
print(lr.score(Xt, yt))"""