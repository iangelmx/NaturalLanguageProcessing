#-*- coding: utf-8 -*-
import nltk
import re
from collections import defaultdict
from nltk.corpus import brown
from pickle import dump
from pickle import load
from functionsNLP import *
import math
from sympy.solvers import solve
from sympy import Symbol


#pText = [0.5*x+(0.5*0.1)]*
#Probabilidad de 'Text'
x = Symbol('x')
#pText = solve( (0.5 - 0.5*x + 0.45)**2 - 0.5*x - 0.05, x)

''' Si subimos la probabilidad de fondo, sube la probabilidad de la 
	palabra en el documento'''
pText = solve( (0.4 - 0.4*x + 0.54)**2 - (0.4*x + 0.06), x)

print("p(text | THETAd): "+str(pText[0]))

#Probabilidd de 'the'
pThe = 1-pText[0]

print("p(the | THETAd)="+str(pThe))

"""tarea:
	Estudiar test_topic_1.py
			 test_topic_2.py
	Lemmatizar, quitar puntuaciones, y quitar stopwords de artículos e960401
	y se mete en test_topic_1.py
	No quitar repeticiones.

"""