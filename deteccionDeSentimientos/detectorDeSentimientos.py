import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WordPunctTokenizer
import sys
from collections import Counter
import numpy
sys.path.insert(0, '../Chapter5')
from mariamysqlib import *
from functionsNLP import *


prepareRawText2Classify("C:\\Users\\iAngelMx\\Documents\\GitHub\\nlp\\deteccionDeSentimientos", tipoRawText = "review", reviewCategory='coches')