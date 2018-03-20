from __future__ import division
import nltk, re, pprint, request
from urllib.request import *
url="http://www.gutenberg.org/files/2554/2554-0.txt"
#url="http://www.gutenberg.org/files/2554/2554.txt"

raw = urlopen(url).read().decode('utf8')
type(raw)
print(len(raw))

print(raw[:75])

tokens = nltk.word_tokenize(raw)
print(len(tokens))
print(tokens[:10])

text=nltk.Text(tokens)
text.collocations()

print(raw.find("PART I"))

print(raw.rfind("End of Project Gutenber's Crime"))

raw=raw[5303:1157743]
print(raw.find("PART I"))


url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
html = request.urlopen(url).read().decode('utf8')
print(html[:60])