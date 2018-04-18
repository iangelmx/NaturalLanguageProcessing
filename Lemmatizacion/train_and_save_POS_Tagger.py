import nltk
from nltk.corpus import cess_esp
from _pickle   import dump

'''train nltk.UnigramTagger using
tagged sentences from cess_esp'''
cess_tagged_sents=cess_esp.tagged_sents()
unigram_tagger=nltk.UnigramTagger(cess_tagged_sents)

'''save the trained tagger in a file '''
output=open('UnigramTagger_cess_esp.pkl', 'wb')
dump(unigram_tagger, output, -1)
output.close()
