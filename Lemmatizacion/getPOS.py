from write import writeList

''' A adjective, R adverb, N noun, V verb, P pronoun, D or T determiner, 
    S adposition, C conjunction, I interjection, F punctuation '''

def divideIntoPOS(filename):
    f=open(filename, 'r', encoding='latin-1')
    lines=f.readlines()
    f.close()
    
    alist=[]
    rlist=[]
    nlist=[]
    vlist=[]
    plist=[]
    dtlist=[]
    slist=[]
    clist=[]
    ilist=[]
    flist=[]

    for line in lines:
        line=line.strip()
        if line != '': 
            words=line.split()
            if words[-2][0] == 'A':  #find adjectives
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                alist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'R':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                rlist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'N':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                nlist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'V':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                vlist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'P':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                plist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'D' or words[-2][0] == 'T':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                dtlist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'S':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                slist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'C':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                clist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'I':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                ilist.append(words[0]+' '+words[-2]+' '+words[-1])
            elif words[-2][0] == 'F':
                if '#' in words[0]: 
                    words[0]=words[0].replace('#','') #eliminate the # symbol
                flist.append(words[0]+' '+words[-2]+' '+words[-1])

    return {'a':alist,'r':rlist,'n':nlist,'v':vlist,'p':plist,'dt':dtlist,'s':slist,'c':clist,'i':ilist,'f':flist}

'''test if run as application'''
if __name__=='__main__':
    diccionario=divideIntoPOS('generate.txt')
    for key in diccionario:
        writeList(diccionario[key],key+'list.txt')
