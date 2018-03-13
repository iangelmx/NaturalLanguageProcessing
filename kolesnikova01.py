import nltk
from bs4 import BeautifulSoup
from write import writeDict
       
def buildRawFreqVectors():
    f1=open('e960401.htm')
    t=f1.read()
    t_lower=t.lower()
     
    '''lxml is the best available HTML parser for BeautifulSoup,
    lxml deletes markup and represents letters with clitics correctly'''
    soup = BeautifulSoup(t_lower, 'lxml')
    text = soup.get_text() 
    tokens=nltk.Text(nltk.word_tokenize(text))
    vocabulary=list(set(tokens))
 
    f2=open('contexts.txt', encoding='utf-8')
    contexts=f2.readlines()
     
    rawFreqVectorsDict={}
     
    for context in contexts:
        words=context.split()
        vector=[]
        for voc in vocabulary:
            if voc in words[1:]:
                vector.append(words[1:].count(voc))
            else:
                vector.append(0)
        rawFreqVectorsDict[words[0]]=vector
 
    return rawFreqVectorsDict
     
'''test if run as application'''
if __name__=='__main__':
    rawFreqVectorsDict=buildRawFreqVectors()
    writeDict(rawFreqVectorsDict, 'rawFrequencyVectors.txt')