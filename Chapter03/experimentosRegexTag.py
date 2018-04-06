# -*- coding: utf-8 -*-
import nltk
import re
from functionsNLP import *
from mariamysqlib import *
import math


[tokens, rawText] = getTextTokens("e960401_txt.txt", backTextString=True)

listaOraciones = separaPorOraciones(rawText)

vocabulary = sorted( set(tokens) )

patterns = [
    (r'.*o$', 'NCMS'),               # Sustantivo Masculino
    (r'.*a$', 'NCFS'),          		 # Sustantivo Femenino
    (r'.*as$', 'NCFP'),
    (r'.*os$', 'NCMP')
]

nltk.corpus.cess_esp.tagged_words()

regexp_tagger = nltk.RegexpTagger(patterns)
oracion = listaOraciones[3]
print(regexp_tagger.tag( nltk.Text(nltk.word_tokenize(oracion)) ))
#print(regexp_tagger.evaluate( nltk.Text(nltk.word_tokenize(oracion)) ))

#print([v for v in vocabulary if re.search(r'(ado|ido)$', v)])



'''

'''
