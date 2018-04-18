def splitIntoFiles(filename, path):
    '''splitIntoFiles(filename) split a file (of adjectives in this module) into 
    smaller files, the name of each smaller file is 
    the first letter in a line of the original file. 
    
    path is the location of the folder where smaller files are to be saved.
    This folder's name is 'A', because in this folder we save files for adjectives.
    The folder 'A' is not created automatically, you have to create it manually.
    
    Remember:
    A adjective, R adverb, N noun, V verb, P pronoun, D or T determiner, 
    S adposition, C conjunction, I interjection, F punctuation.'''

    f=open(filename, 'r', encoding='utf-8')
    lines=f.readlines()
    f.close()
           
    for line in lines:
        line=line.strip()
        words=line.split()
        if len(words[0])==1:
            output = open(path+words[0]+'.txt', 'a')
            output.write(line+'\n')
            output.close()
        elif len(words[0])>1:    
            #print(words[0])
            output = open(path+words[0][0:2]+'.txt', 'a')
            output.write(line+'\n')
            output.close()
    
'''test if run as application'''
if __name__=='__main__':
    splitIntoFiles(
    'C:\\Users\\OLGA\\Pprog_work\\NLP_2018_2_programs\\Lemmatization\\adjectives.txt',
    'C:\\Users\\OLGA\\Pprog_work\\NLP_2018_2_programs\\Lemmatization\\A\\')
    
