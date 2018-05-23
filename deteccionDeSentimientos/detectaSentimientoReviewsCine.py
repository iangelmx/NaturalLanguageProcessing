import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
import sys
from collections import Counter
import numpy
sys.path.insert(0, '../Chapter5')
from functionsNLP import *
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split

dirpath = os.getcwd()
#"C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\deteccionDeSentimientos"
[sampleTexts,y] = prepareRawText2Classify(dirpath, tipoRawText = "reviewCine")
y=np.asarray(y)

#y<- etiquetas de los textos
#X<- Lista de características
count_vect = CountVectorizer()
X_counts = count_vect.fit_transform(sampleTexts)
X=X_counts

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state = 42)

import mord as m

clf = m.LogisticIT()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

archivo = open('resultados.txt', "w")

from sklearn import metrics
print("Precisión de prediccion: ",clf.score(X_test, y_test))
print("Matriz de confusión: \n",metrics.confusion_matrix(y_test, y_pred))
print("Classification report: \n", metrics.classification_report(y_test, y_pred))

archivo.write("Precisión de prediccion: \n")
archivo.write(str(clf.score(X_test, y_test)))
archivo.write("\nMatriz de confusión: \n")
archivo.write(metrics.confusion_matrix(y_test, y_pred).tostring())
archivo.write("\nClassification report: \n")
archivo.write(metrics.classification_report(y_test, y_pred).tostring())

archivo.close()