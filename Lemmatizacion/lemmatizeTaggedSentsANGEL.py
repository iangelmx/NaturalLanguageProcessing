import nltk
from _pickle import load
from bs4   import BeautifulSoup
from mariamysqlib import *


def lemmatizerBD2(rutaArchivoLemmas, tabla):
    recoverFromDB = doQuery("SELECT token FROM "+tabla+" ORDER BY idToken;")
    if recoverFromDB:
        tokens=[]
        for elemento in recoverFromDB:
            tokens.append(elemento[0])
    lemmas = open(rutaArchivoLemmas, mode="r")#, encoding="utf-8")
    transaccion = []
    transaccion.append("START TRANSACTION;")
    cadena=lemmas.readline()
    conteo=0
    while cadena != '':
        try:
            cadena = cadena.split(' ')
            forma = cadena[0]
            #print("...."+str(cadena[1]))
            etiqueta = cadena[1]
            lemma = cadena[len(cadena)-2]
            forma = forma.replace('#', '')
            #print("Forma lema-> "+forma+" "+lemma)
            if (forma in tokens) and (etiqueta[0]=='N' or etiqueta[0]=='n'):
                #print("Es sustantivo: "+forma+" - "+lemma)
                transaccion.append("UPDATE "+tabla+" SET lemmaToken='"+lemma+"' WHERE token ='"+forma+"'")
            """else:
                    print("Se ignoró: "+forma+" - "+lemma)"""
            if conteo % 100000 == 0:
                print("Actualizando Tokens Conteo-> "+str(conteo))
            cadena=lemmas.readline()
            conteo+=1
        except Exception as ex:
            print(ex)
            cadena=lemmas.readline()
            pass
    transaccion.append("COMMIT;")
    return doTransaction(transaccion)



'''This module lemmatizes tagged sentences from the file 'example.htm'
which is a small part of the file 'e960401.htm' 
Before running this module, you have to train a tagger and save it in a file.
This is done by the module 'train_and_save_POS_tagger.py' '''

def lemmatizeTaggedSents(fname, isHtml=True, getNouns=False):
    taggedSents=tagSents(fname, isHtml)
    
    lemmas=[]
    for sent in taggedSents:
        lemSent=[]
        for taggedword in sent:
            if taggedword[1]==None or taggedword[1][0]=='F':
                lemSent.append(taggedword[0])
            else:
                #print("Taged word->" + str(taggedword))
                if getNouns==True:
                    if taggedword[1][0]=='N' or taggedword[1][0]=='n':
                        lemma=getLemma(taggedword[0], taggedword[1][0])
                        #input(lemma)
                        if lemma=='':
                            lemSent.append(taggedword[0])
                        else:
                            lemSent.append(lemma)
                else:
                    lemma=getLemma(taggedword[0], taggedword[1][0])
                    #input(lemma)
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
    else:
        cadena = fname
        #print("->"+str(cadena))
    textString=cadena.lower()

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
    import sys
    import string
    
    exclude = set(string.punctuation)
    exclude.update(['¿', '¡', '"'])

    # argumento = sys.argv[1:]
    # cadenaArgumento = ' '.join(argumento)

    #archivoIn = open("cadenaGeneralReviewsMoviles.txt", "r")
    archivoIn = open("cadenaGeneralReviewsMovilesNormalizada.txt", "r")
    cadenaArgumento = archivoIn.read()
    
    #input(cadenaArgumento)


    lemmas=lemmatizeTaggedSents(cadenaArgumento, isHtml=False)
    lemmasNouns=lemmatizeTaggedSents(cadenaArgumento, isHtml=False, getNouns=True)

    """entrada = open("salidaFIN.txt", mode="r", encoding="utf-8")
    rawTokens = entrada.read()
    entrada.close()

    rawTokens=rawTokens.replace(',','').replace("'", '')
    rawTokens=rawTokens.replace('[','').replace(']', '')
    rawTokens = rawTokens.split()"""

    #input("Lemmas->"+str(lemmas))

    """transaccion=[]
                transaccion.append("START TRANSACTION;")
                transaccion.append("TRUNCATE tokens_Lemmatizados;")
                for lemma in lemmas:
                    input("Lemma->"+str(lemma))
                    transaccion.append("INSERT into tokens_Lemmatizados(token) VALUES('"+lemma+"')")
                transaccion.append("COMMIT;")
            
                resul = doTransaction(transaccion)
                print(resul)"""

    transaccion=[]
    transaccion.append("START TRANSACTION;")
    transaccion.append("TRUNCATE lemmasReviewsMoviles;")
    for listaLemmas in lemmas:
        for lemma in listaLemmas:
            lemma = ''.join(char for char in lemma if char not in exclude)
            if lemma not in exclude:
                transaccion.append("INSERT into lemmasReviewsMoviles(lemmaReviewMovil) VALUES('"+lemma+"');")
    transaccion.append("COMMIT;")

    resul = doTransaction(transaccion)#, traceback=True)
    print(resul)

    transaccion=[]
    transaccion.append("START TRANSACTION;")
    transaccion.append("TRUNCATE nounsReviewsMoviles;")
    for listaLemmas in lemmasNouns:
        for noun in listaLemmas:
            noun = ''.join(char for char in noun if char not in exclude)
            if noun not in exclude:
                transaccion.append("INSERT into nounsReviewsMoviles(lemmaNoun) VALUES('"+noun+"');")
    transaccion.append("COMMIT;")

    # for elem in transaccion:
    #     print(elem)

    resul = doTransaction(transaccion)
    print(resul)

    #archivo = open('salidaFIN.txt', "w")
    #archivo.write(str(lemmas))
    #archivo.close()
   
  
    
