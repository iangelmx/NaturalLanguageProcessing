import nltk
import sys
import numpy
from sklearn.naive_bayes import MultinomialNB
sys.path.insert(0, '../Chapter5')
#sys.path.insert(0, '../Chapter5')
from mariamysqlib import *
from functionsNLP import *

print(doQuery("SELECT 'hola' FROM dual;"))

X = numpy.random.randint(5, size=(6, 100))
y = numpy.array([1, 2, 3, 4, 5, 6])

clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
#Si alpha = 1, es Laplace
#Si fit_prior = True, se hace el conteo de palabras en la suma de todas

clf.fit(X,y)

print(clf.predict(X[2:3]))
##X[De dos a dos]


#Conteo relativo.
#Probabilidad de la palbra en una categoría, no en un documento.

"""
MultinomialNB <-scikit
BinomialNB <- scikit
GaussianNB
"""
#Lemmatizar y quitar stopwords <- Creo que no es de tarea
#Como hacer representación vectorial de texto en Numpy.