def writeList(myList, fname):
    '''writeList(myList, fname) writes list to text file'''
    f = open(fname, "w", encoding="utf-8")#open a UTF-8 text file for writing
    for i in range(len(myList)):
        f.write(str(myList[i])+'\n') 
    f.close()
    print('Message of writeList(myList, fname): The list in '+fname+' has '+str(len(myList))+' lines.')
 
def writeDict(myDict, fname):
    '''writeDict(myDict, fname) writes dictionary to text file'''
    f = open(fname, "w", encoding="utf-8")#open a UTF-8 text file for writing
    for key, value in myDict.items():
        f.write('%s ' % (key))
        for i in range(len(list(value))):
            f.write('%s ' % (list(value)[i]))
        f.write('\n')
    f.close()
   
def writeListOfLists(myList, fname):
    ''' writeListOfLists(myList, fname) writes list of lists to text file'''
    f = open(fname, "w", encoding="utf-8")#open a UTF-8 text file for writing, "a" for append
    for i in range(len(myList)):
        w=myList[i]
        for j in range(len(w)):
            f.write(w[j]+' ')
        f.write('\n')
    f.close()
    print('Message of writeListOfLists(myList, fname): The list in '+fname+' has '+str(len(myList))+' lines.')
 
'''test if run as application'''
if __name__=='__main__':
    pass
     