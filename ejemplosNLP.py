#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import nltk
#nltk.download()

#pp4
from __future__ import division
from nltk.book import *
import matplotlib

print("text1->"+str(text1)+"\n")
print("text2->"+str(text2)+"\n")
print("\n-----------------\n")
print("...")
print(text1.concordance("monstrous"))
print("\n-----------------\n")

#pp5

print(text1.similar("monstrous"))
print("")
print(text2.similar("monstrous"))
text2.similar("life")

print("Abajo")
print(text2.common_contexts(["monstrous", "very"]))
print("Arriba")
#pp6
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
#pp7

text3.generate(words="citizens")

print("Longitud Texto 3: "+str(len(text3)))

#pp8
print(sorted(set(text3)))

print(len(set(text3)))


#from __future__ import division

print("After Future: "+ str(len(text3)/len(set(text3))) )

print("t3.count('smote') -> "+str(text3.count("smote")) )

print("t4.count('a') -> "+str(100*text4.count('a')/len(text4)) )


#pp9
def lexical_diversity(text):
	return len(text)/len(set(text))

def percentage(count, total):
	return 100*count/total


print("lexical diversity t3-> "+str(lexical_diversity(text3)))

print("lexical diversity t5-> "+str(lexical_diversity(text5)))

print("Percentage -> "+str(percentage(4,5)))
print("Percentage t4.count, len(text4) -> "+str(percentage(text4.count('a'), len(text4))))

#pp10

sent1=['Call', 'me', 'Ishmael','.']
print(sent1)
print("Lenght sent1 : "+str(len(sent1)))
print("lex_div -> "+str(sent1))

#pp11
print(sent2)
print(sent3)


print("sent4 + sent1-> "+str(sent4 + sent1))
sent1.append("Some")
print(sent1)

#pp12 indexing

print("text4[173]-> "+str(text4[173]))
print("text4.index('awaken')-> "+str(text4.index('awaken')))

print("sent4-> "+str(sent3[:3]))

my_sent = ['Bravely', 'bold', 'Sir', 'Robin', ',', 'rode']

