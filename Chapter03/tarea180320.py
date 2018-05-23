#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import os
import nltk, re, pprint
from urllib.request import *
from bs4 import BeautifulSoup
import feedparser
#from functionsNLP import *
import sys
sys.path.insert(0, '../aramirezaNlpLib')
from iangelmxNlpLib import *
url="http://www.gutenberg.org/files/2554/2554-0.txt"
#url="http://www.gutenberg.org/files/2554/2554.txt"

texto="Hola a todos. ¿Cómo se encuentran el día de hoy?. Espero que muy bien, ya que yo estoy muy contento de verlos."
print(separaPorOraciones(texto))

"""
raw = urlopen(url).read().decode('utf8')
type(raw)
print(len(raw))

print(raw[:75])

tokens = nltk.word_tokenize(raw)
print(len(tokens))
print(tokens[:10])
"""

#text=nltk.Text(tokens)
[tokens, cadena] = getTextTokens("e960401_txt.txt", backTextString=True)

text=nltk.Text(tokens)
#raw = unicode(cadena, "utf-8")
raw = cadena.encode("utf-8")
text.collocations()
print("")
lista = separaPorOraciones(cadena)

for elemento in lista:
	print(elemento)

input("Fin")

#text.collocations()

print(raw.find("PART I"))

print(raw.rfind("End of Project Gutenber's Crime"))

raw=raw[5303:1157743]
print(raw.find("PART I"))


url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = urlopen(url).read().decode('utf8')
print(html[:60])

raw = BeautifulSoup(html, 'lxml').get_text()
tokens = nltk.word_tokenize(raw)
print(tokens)

	
tokens = tokens[110:390]
text = nltk.Text(tokens)
text.concordance('gene')

#--------------------------
#Processing RSS Feeds
print("------------\n#Processing RSS Feeds\n------------")

llog=feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
print(":v")
print(llog['feed']['title'])
print(len(llog.entries))
print("Qué hizo?")
post = llog.entries[2]
print(post.title)

content = post.content[0].value
print(content[:70])

raw = BeautifulSoup(content,'lxml').get_text()
print(nltk.word_tokenize(raw))

cadena="Hola a "\
		"todos en el mundo"

print(cadena)