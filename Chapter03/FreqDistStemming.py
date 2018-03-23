# -*- coding: utf-8 -*-
from functionsNLP import *
from mariamysqlib import *

[tokens, abc]=getTextTokens("e960401_txt.txt", backTextString=True)

stopwordslist = set(stopwords.words('spanish'))
#guardaEnArchivo("OUT_FILES\VocabularioSinNumeros.txt", textoTokenizado)

textoTokenizadoNoStopWords = [word for word in tokens if word not in stopwordslist]