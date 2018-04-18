from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from mariamysqlib import *
from functionsNLP import *

#example documents
'''doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle." '''

''' A adjective, R adverb, N noun, V verb, P pronoun, D or T determiner, 
    S adposition, C conjunction, I interjection, F punctuation '''

def lematizaBDArts(tokensEtiquetados):
	lemmas = open("generate.txt", mode="r")#, encoding="utf-8")
	transaccion = []
	transaccion.append("START TRANSACTION;")
	cadena=lemmas.readline()
	conteo=0
	while cadena != '':
		try:
			cadena = cadena.strip()
			cadena = cadena.split(' ')
			forma = cadena[0]
			etiqueta = cadena[-2]
			lemma = cadena[-1]
			forma = forma.replace('#', '')
			#print("lemma: "+lemma+ " | TAG: "+ etiqueta +" | Forma: "+forma)

			if etiqueta[0] == 'a' or etiqueta[0] =='A':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'A%' );")
			elif etiqueta[0] == 'r' or etiqueta[0] =='R':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'R%' );")
			elif etiqueta[0] == 'n' or etiqueta[0] =='N':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'N%' );")
			elif etiqueta[0] == 'v' or etiqueta[0] =='V':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'V%' );")
			elif etiqueta[0] == 'p' or etiqueta[0] =='P':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'P%' );")
			elif etiqueta[0] == 'd' or etiqueta[0] =='D' or etiqueta[0] == 't' or etiqueta[0] =='T':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'D%' OR tag LIKE 'T%');")
			elif etiqueta[0] == 's' or etiqueta[0] =='S':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'S%' );")
			elif etiqueta[0] == 'c' or etiqueta[0] =='C':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'C%' );")
			elif etiqueta[0] == 'i' or etiqueta[0] =='I':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'I%' );")
			elif etiqueta[0] == 'f' or etiqueta[0] =='F':
				transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'F%' );")

			for lista in tokensEtiquetados:
				if (etiqueta[0] == 'a' or etiqueta[0] =='A') and (lista[1][0]== 'a' or lista[1][0] =='A') and (lista[0] == forma):
					lista[0] = lemma
				elif (etiqueta[0] == 'r' or etiqueta[0] =='R') and (lista[1][0]== 'r' or lista[1][0] =='R') and (lista[0] == forma):
					lista[0] = lemma
				elif (etiqueta[0] == 'n' or etiqueta[0] =='N') and (lista[1][0]== 'n' or lista[1][0] =='N') and (lista[0] == forma):
					lista[0] = lemma
				elif (etiqueta[0] == 'v' or etiqueta[0] =='V') and (lista[1][0]== 'v' or lista[1][0] =='V') and (lista[0] == forma):
					lista[0] = lemma
				elif (etiqueta[0] == 'p' or etiqueta[0] =='P') and (lista[1][0]== 'p' or lista[1][0] =='P') and (lista[0] == forma):
					lista[0] = lemma
				elif (etiqueta[0] == 'd' or etiqueta[0] =='D') or etiqueta[0] == 't' or etiqueta[0] =='T') and (lista[1][0]== 'p' or lista[1][0] =='P') and (lista[0] == forma):
					transaccion.append("UPDATE tokens_tags SET token='"+lemma+"' WHERE token= '"+forma+"' AND (tag LIKE 'D%' OR tag LIKE 'T%');")
				elif etiqueta[0] == 's' or etiqueta[0] =='S':
					lista[0] = lemma
				elif etiqueta[0] == 'c' or etiqueta[0] =='C':
					lista[0] = lemma
				elif etiqueta[0] == 'i' or etiqueta[0] =='I':
					lista[0] = lemma
				elif etiqueta[0] == 'f' or etiqueta[0] =='F':
					lista[0] = lemma


			if conteo % 100000 == 0:
				print("Actualizando Tokens Conteo-> "+str(conteo))
			cadena=lemmas.readline()
			conteo+=1
		except Exception as ex:
			print(ex)
			cadena=lemmas.readline()
			pass
	transaccion.append("COMMIT;")
	print(doTransaction(transaccion))

#lematizaBDArts()

arts = doQuery("SELECT cuerpo FROM articulos ORDER BY id LIMIT 2;")
cadenaDocs = ""
documentos = []

archivoStop = open("stopwords_es.txt", mode="r", encoding="utf-8")
stopWordsEsp = []

cadena=archivoStop.readline()
while cadena!= '':
	cadena=cadena.replace('\n','')
	stopWordsEsp.append(cadena)
	cadena=archivoStop.readline()
	#print(cadena)

for art in arts:
	documentos.append(art[0])
	cadenaDocs+=art[0]
	cadenaDocs+="\n\n"

listaOraciones = separaPorOraciones(cadenaDocs)
tokensEtiquetados = tagRawText2POS(listaOraciones)

transaccion = []
transaccion.append("START TRANSACTION;")
transaccion.append("TRUNCATE tokens_tags;")
for elemento in tokensEtiquetados:
	transaccion.append("INSERT INTO tokens_tags(token, tag) VALUES('"+str(elemento[0])+"','"+str(elemento[1])+"');")
transaccion.append("COMMIT;")



print(doTransaction(transaccion))
lematizaBDArts(tokensEtiquetados)

input("¿¿¿¿???????")
input()




doc_complete = documentos

# compile documents
######doc_complete = [doc1, doc2, doc3, doc4, doc5]

#clean documents
####stop = set(stopwords.words('english'))
#---------------stop = set(stopwords.words('spanish'))
#print("........\n"+str(stop)+"\n-------------")
stop = stopWordsEsp

#input(stop)

exclude = set(string.punctuation)

lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete] 

'''Creating the term dictionary of our courpus, where every unique term is assigned an index.'''
dictionary = corpora.Dictionary(doc_clean)

#doc_clean deben ser nuestros datos.

'''Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.'''
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

'''Creating the object for LDA model using gensim library'''
Lda = gensim.models.ldamodel.LdaModel

'''Running and Trainign LDA model on the document term matrix.'''
ldamodel = Lda(doc_term_matrix, num_topics=5, id2word = dictionary, passes=50)

print(ldamodel.print_topics(num_topics=5, num_words=10))

""" 
TAREA:
	LEMMATIZAR 2 ARTICULOS CON EL GENERATE.TXT POR PARTES DE ORACION
"""