import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
import sys
from collections import Counter
import numpy
sys.path.insert(0, '../Chapter5')
from mariamysqlib import *
from functionsNLP import *
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split

print(""" Posibles clases: 
	1) """)
categoria = input("Teclee la categoría a evaluar (1-> Positive 0-> Negative)")

[sampleTexts,y] = prepareRawText2Classify("C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\deteccionDeSentimientos", tipoRawText = "review", reviewCategory=categoria)

y=np.asarray(y)

count_vect = CountVectorizer()
X_counts = count_vect.fit_transform(sampleTexts)
X=X_counts

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)

import mord as m

clf = m.LogisticIT()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

from sklearn import metrics
print("Precisión de prediccion: ",clf.score(X_test, y_test))
print("Matriz de confusión: \n",metrics.confusion_matrix(y_test, y_pred))
print("Classification report: \n", metrics.classification_report(y_test, y_pred))
