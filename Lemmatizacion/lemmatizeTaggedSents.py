import nltk
from _pickle import load
from bs4   import BeautifulSoup
from mariamysqlib import *

'''This module lemmatizes tagged sentences from the file 'example.htm'
which is a small part of the file 'e960401.htm' 
Before running this module, you have to train a tagger and save it in a file.
This is done by the module 'train_and_save_POS_tagger.py' '''

def lemmatizeTaggedSents(fname):
    taggedSents=tagSents(fname)
    
    lemmas=[]
    for sent in taggedSents:
        lemSent=[]
        for taggedword in sent:
            if taggedword[1]==None or taggedword[1][0]=='F':
                lemSent.append(taggedword[0])
            else:
                lemma=getLemma(taggedword[0], taggedword[1][0])
                if lemma=='':
                    lemSent.append(taggedword[0])
                else:
                    lemSent.append(lemma)
        lemmas.append(lemSent)
    return lemmas

def getLemma(wordform, pos):
    lemma=''
    if len(wordform)==1:
        try:
            f=open(pos.upper()+'\\'+wordform[0]+'.txt')
            lines=f.readlines()
            f.close()
            for line in lines:
                line=line.strip()
                words=line.split()
                if words[0]==wordform:
                    lemma=words[-1]
        except FileNotFoundError:
            pass
    elif len(wordform)>1:
        try:
            f=open(pos.upper()+'\\'+wordform[0:2]+'.txt')
            lines=f.readlines()
            f.close()
            for line in lines:
                line=line.strip()
                words=line.split()
                if words[0]==wordform:
                    lemma=words[-1]
        except FileNotFoundError:
            pass
    return lemma
                            
def tagSents(fname, isHtml=True):
    if isHtml==True:
        f=open(fname)
        t=f.read()
        soup = BeautifulSoup(t, 'lxml')
        textString = soup.get_text()
    textString=textString.lower()

    '''get a list of sentences'''
    sent_tokenizer=nltk.data.load('nltk:tokenizers/punkt/english.pickle')
    sents=sent_tokenizer.tokenize(textString)

    '''download the tagger'''
    input=open('UnigramTagger_cess_esp.pkl', 'rb')
    tagger=load(input)
    input.close()

    '''tag sentences, a tagged sentence is a list of tuples,
    each tuple includes 2 elements'''
    taggedSents=[]
    for sent in sents:
        tagged_sent=tagger.tag(nltk.word_tokenize(sent))
        taggedSents.append(tagged_sent)
    
    return taggedSents
 
'''test if run as application'''
if __name__=='__main__':
    
    lemmas=lemmatizeTaggedSents('e960401.htm', isHtml=False)

    """entrada = open("salidaFIN.txt", mode="r", encoding="utf-8")
    rawTokens = entrada.read()
    entrada.close()

    rawTokens=rawTokens.replace(',','').replace("'", '')
    rawTokens=rawTokens.replace('[','').replace(']', '')
    rawTokens = rawTokens.split()"""

    transaccion=[]
    transaccion.append("START TRANSACTION;")
    transaccion.append("TRUNCATE tokens_Lemmatizados;")
    for lemma in lemmas:
        transaccion.append("INSERT into tokens_Lemmatizados(token) VALUES('"+lemma+"')")
    transaccion.append("COMMIT;")

    resul = doTransaction(transaccion)
    print(resul)

    #archivo = open('salidaFIN.txt', "w")
    #archivo.write(str(lemmas))
    #archivo.close()
   
  
    
