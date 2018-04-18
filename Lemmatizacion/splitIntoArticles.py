import re
from bs4 import BeautifulSoup

def splitIntoArticles(fname):
    f=open(fname, 'r', encoding='latin-1') 
    t=f.read()
    f.close()
  
    articles=re.split('<h3>', t)
    
    arts=[]
    #clean articles from html tags
    for article in articles:
        soup = BeautifulSoup(article, 'lxml') #article is a string
        text = soup.get_text()
        text=text.replace(u'\x97', '') #remove the problematic symbol from the text string 
        arts.append(text)
    
    return arts #a list of strings, each string is an article

'''test if run as application'''
if __name__=='__main__':
    articles=splitIntoArticles('example.htm')
   


    
    
    









