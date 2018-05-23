#-*- coding: utf-8 -*-
import nltk
import re
from collections import defaultdict
from nltk.corpus import brown
from pickle import dump
from pickle import load
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *


""" 
Ejercicio:
Entrenar un etiquetador de NLTK nltk.UnigramTagger con oraciones de cess_esp
Oración 10 del archivo e960401 
"""
[tokens, rawText] = getTextTokens("e960401_txt.txt", backTextString=True)

listaOraciones = separaPorOraciones(rawText)


esp=nltk.corpus.cess_esp.tagged_words()

#size = int(len(listaOraciones) * 0.9)
train_sents = listaOraciones[10]

nltk.corpus.cess_esp.tagged_words()

patterns = [
    (r'.*o$', 'NCMS'),               # Sustantivo Masculino
    (r'.*a$', 'NCFS'),          		 # Sustantivo Femenino
    (r'.*as$', 'NCFP'),
    (r'.*os$', 'NCMP')
]

regexp_tagger = nltk.RegexpTagger(patterns)
cess_tagged_sents = nltk.corpus.cess_esp.tagged_sents()

oracion = listaOraciones[10]
oracionTokenizada = nltk.Text(nltk.word_tokenize(oracion))

var = regexp_tagger.tag( oracionTokenizada )

""" Training nltk.UnigramTagger usando oraciones desde cess_esp """
unigram_tagger = nltk.UnigramTagger( cess_tagged_sents, backoff=nltk.RegexpTagger(patterns))

example = unigram_tagger.tag(oracionTokenizada)

print(example)

"""print(unigram_tagger.evaluate(train_sents))"""

##print(regexp_tagger.tag( nltk.Text(nltk.word_tokenize(train_sents)) ))

"""
Extraer todos los sustantivos de e960401, lematizarlos y aplicar set()
Si empieza con n, se obtiene la palabra.
"""