from gensim import corpora, models
from itertools import chain
from mariamysqlib import *

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

documentos = doQuery("SELECT cuerpo FROM articulos")
docs = []
b=0
tokens = []
longitudes =[]

for a in documentos:
    docs.append(a[0])
    """tokens.append(nltk.word_tokenize(a[0]))
    longitudes.append(len( nltk.word_tokenize(a[0]) ))"""

'''remove common words and tokenize'''
#CAMBIAR la lista de stop words por la del archivo generate :v
###stoplist = set('for a of the and to in'.split())
archivoStop = open("stopwords_es.txt", mode="r", encoding="utf-8")
stopWordsEsp = []

cadena=archivoStop.readline()
while cadena!= '':
    cadena=cadena.replace('\n','')
    stopWordsEsp.append(cadena)
    cadena=archivoStop.readline()

stoplist=stopWordsEsp

texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in docs]

'''remove words that appear only once'''
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

'''Create Dictionary'''
id2word = corpora.Dictionary(texts)

'''Create the Bag of Word corpus'''
mm = [id2word.doc2bow(text) for text in texts]

'''Train the LDA models'''
lda = models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=3, \
                               update_every=1, chunksize=10000, passes=1)

'''Print the topics'''
for top in lda.print_topics():
    print(top)
print()

'''Assign the topics to the documents in corpus'''
lda_corpus = lda[mm]

'''Find the threshold, let's set the threshold to be 1/#clusters,
To prove that the threshold is sane, we average the sum of all probabilities'''
scores = list(chain(*[[score for topic_id,score in topic] \
                      for topic in [doc for doc in lda_corpus]]))
threshold = sum(scores)/len(scores)
print(threshold)
print()

cluster1 = [j for i,j in zip(lda_corpus,docs) if i[0][1] > threshold]
cluster2 = [j for i,j in zip(lda_corpus,docs) if i[1][1] > threshold]
cluster3 = [j for i,j in zip(lda_corpus,docs) if i[2][1] > threshold]

print(cluster1)
print(cluster2)
print(cluster3)

"""
"""