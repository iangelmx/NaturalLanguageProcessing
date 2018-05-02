import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords 
import sys
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
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

archivo = open("SMS_Spam_Corpus.txt", "r")
stop = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()
mensaje = archivo.readline()

#tokensGrales = tokenizaFrase(leeArchivo("SMS_Spam_Corpus.txt"), wordPunct=True)
[tokensGrales, rawText] = getTextTokens("SMS_Spam_Corpus.txt",backTextString=True)
tokensGrales= set(tokensGrales)

print(":v")
mensajesLemmasSPAM = []
mensajesLemmasHAM = []
mensajesTotales = []
while mensaje != '':
	if mensaje:	
		try:
			if 'spam' in mensaje.split()[-1]:
				mensaje=mensaje.replace(',spam', '')
				fraseTokenizada = tokenizaFrase(mensaje, wordPunct=True)
				mensajeLemmatizado = []
				for token in fraseTokenizada:
					tokenLemmatizado = wordnet_lemmatizer.lemmatize(token, pos='v')
					mensajeLemmatizado.append(tokenLemmatizado)
				mensajesLemmasSPAM.append(mensajeLemmatizado)
				#print("SPAM "+str(mensajeLemmatizado)+"\n")
			elif 'ham' in mensaje.split()[-1]:
				mensaje=mensaje.replace(',ham', '')
				fraseTokenizada = tokenizaFrase(mensaje, wordPunct=True)
				mensajeLemmatizado = []
				for token in fraseTokenizada:
					tokenLemmatizado = wordnet_lemmatizer.lemmatize(token, pos='v')
					mensajeLemmatizado.append(tokenLemmatizado)
				mensajesLemmasHAM.append(mensajeLemmatizado)
				#print("HAM"+str(mensajeLemmatizado)+"\n")
			else:
				input("Mensaje con contenido desconocido... ->"+str(mensaje.split()[-1])+ "<-")
			mensajesTotales.append(mensajeLemmatizado)
		except Exception as ex:
			print(ex)
	mensaje = archivo.readline()

"""vector = CountVectorizer()
#noticias = fetch_20newsgroups(subset='train')
#print("Tipo de dato de noticias.data-> "+str(type(noticias.data)))
input()

mensajesLemmatizadosStrings = []

for lista in mensajesTotales:
	cadena = " ".join(lista)
	print(cadena)
	mensajesLemmatizadosStrings.append(cadena)

vector.fit(mensajesLemmatizadosStrings)

#print(vector.vocabulary_)
bolsa = vector.transform(mensajesLemmatizadosStrings)
print("Tamaño Bag of Words -> "+str(bolsa.shape))
ocurrenciasDict = nltk.FreqDist(tokensGrales)
print(ocurrenciasDict)
valoresOcurrencias=list(ocurrenciasDict.values())
print("VALORES...")
print(ocurrenciasDict.values())
bolsaY = numpy.array(valoresOcurrencias)
print(bolsaY)
Xe, Xt, ye, yt = train_test_split(bolsa, bolsaY)"""



dictionary = Counter(tokensGrales)
print("Diccionario->"+str(dictionary))


clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
#Si alpha = 1, es Laplace
#Si fit_prior = True, se hace el conteo de palabras en la suma de todas

##clf.fit(Xe,ye)

##print(clf.predict(X[2:3]))

"""input(":v:v:v:v")
input()

lr = LogisticRegression()
lr.fit(Xe, ye)
print(lr.score(Xt, yt))"""