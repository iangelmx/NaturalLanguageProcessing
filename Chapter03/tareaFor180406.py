# -*- coding: utf-8 -*-
import nltk
import re
from functionsNLP import *
from mariamysqlib import *
from collections import defaultdict
from nltk.corpus import brown

pos = defaultdict(list)

pos['a']=['1', '2', '3']
pos['b']=['6','7']

print(pos)

pos = defaultdict(lambda: 'NOUN')

print(list(pos.items()))
print("")


brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')

patterns = [
    (r'.*ing$', 'VBG'),               # gerunds
    (r'.*ed$', 'VBD'),                # simple past
    (r'.*es$', 'VBZ'),                # 3rd singular present
    (r'.*ould$', 'MD'),               # modals
    (r'.*\'s$', 'NN$'),               # possessive nouns
    (r'.*s$', 'NNS'),                 # plural nouns
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
    (r'.*', 'NN')                     # nouns (default)
]

regexp_tagger = nltk.RegexpTagger(patterns)
print(regexp_tagger.tag(brown_sents[3]))
print(regexp_tagger.evaluate(brown_tagged_sents))



