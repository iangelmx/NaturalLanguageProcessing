# -*- coding: utf-8 -*-
import nltk
import re
from collections import defaultdict
from nltk.corpus import brown
from pickle import dump
from pickle import load
import sys
sys.path.insert(0, '../Chapter03/mariamysqlib.py')
sys.path.insert(0, '../Chapter03/functionsNLP.py')



"""from functionsNLP import *
from mariamysqlib import *"""

brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')
unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
print(unigram_tagger.tag(brown_sents[2007]))

print(".-.-.-.-.-")

print(unigram_tagger.evaluate(brown_tagged_sents))


size = int(len(brown_tagged_sents) * 0.9)
print(size)
train_sents = brown_tagged_sents[:size]
test_sents = brown_tagged_sents[size:]
unigram_tagger = nltk.UnigramTagger(train_sents)
print(unigram_tagger.evaluate(test_sents))


bigram_tagger = nltk.BigramTagger(train_sents)
print(bigram_tagger.tag(brown_sents[2007]))


unseen_sent = brown_sents[4203]
print(bigram_tagger.tag(unseen_sent))

#Multiple tagging

t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(train_sents, backoff=t0)
t2 = nltk.BigramTagger(train_sents, backoff=t1)


print("Conjuntando varios taggers")

print(t2.evaluate(test_sents))

##E######

output = open('t2.pkl', 'wb')
dump(t2, output, -1)
output.close()

input = open('t2.pkl', 'rb')
tagger = load(input)
input.close()
 	
text = """The board's action shows what free enterprise
    is up against in our complex maze of regulatory laws ."""
tokens = text.split()
print(tagger.tag(tokens))