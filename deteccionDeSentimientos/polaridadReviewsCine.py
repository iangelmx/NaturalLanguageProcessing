#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
from collections import Counter
import numpy
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
from mariamysqlib import *
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split

dirpath = os.getcwd()
#"C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\deteccionDeSentimientos"
rutaCorpusPolaridad = "C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\Corpus\\ML-SentiCon"
rutaCorpusPolaridad = "C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\Corpus\\ML-SentiCon"

transaccion = prepareRawText2Classify(dirpath, tipoRawText = "reviewCine", maxReviews=500, rutaDiccionarioPolaridad=rutaCorpusPolaridad, polaridad=True)
#transaccion = prepareRawText2Classify(dirpath, tipoRawText = "reviewCine", rutaDiccionarioPolaridad=rutaCorpusPolaridad, polaridad=True)
resultado = doTransaction(transaccion) #, traceback=True)

print(resultado)
