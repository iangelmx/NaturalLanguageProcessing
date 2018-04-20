import pymysql												#Para conectarse a la base de datos de mysql

hostname="localhost"
username="root"
password="Trun0k2SAg"
database="nlp"

def updateInDB(table,upParams,upValue, whereParams, whereValues):
	myConnection =pymysql.connect( host=hostname, user=username, passwd=password, db=database )	#Crear la conexión con la BD
	cur = myConnection.cursor()
	myQuery="UPDATE "+table+" SET "

	for param, value in zip(upParams,upValue):#Agregar la lista de cambios separados por comas
		myQuery+=param+"='"+value+"',"
	myQuery = myQuery[:-1] + " WHERE " #Quitar la última coma y preparar para las condiciones

	for param, value in zip(whereParams,whereValues):#Agregar la lista de parámetros separada por comas
		myQuery+=param+"='"+value+"',"
	myQuery = myQuery[:-1] + ";" #Quitar la última coma y preparar para los parámetros

	print("RM-> Query: "+myQuery)
	cur.execute( myQuery )
	myConnection.commit()
	
	result=cur.fetchall()

	myConnection.close()
	print(str(result))
	return True #MEJORA ISSSUE 14	
def existsInDB(table,params,values):#Checa si existe un elemento con un valor value en un parametro param dentro de la tabla table. Si existr rgresa True, sino False
	
	query="SELECT COUNT(1) FROM "+table +" WHERE "
	for param, value in zip(params,values):#Agregar la lista de cambios separados por comas
		query+=param+"='"+value+"' AND "
	query=query[:-4]
	print("RM-> Exists Query: "+query)
	#+param+" = '"+value+"'"#Un query para contar las veces que se repite un param de valor value en table
	amount=doQuery(query)
	if str(amount[0][0])=="0":#Si no existe
		return False
	return True	#Si existe
def insertInDB(table, parameters, values, trace=True):#Inserta un nuevo elemento en la BD, los parametros van en forma de lista al igua que los valores regra
	myConnection =pymysql.connect( host=hostname, user=username, passwd=password, db=database, charset='utf8' )	#Crear la conexión con la BD
	cur = myConnection.cursor()
	myQuery="INSERT INTO "+table+" ( "
	
	for param in parameters:#Agregar la lista de parámetros separada por comas
		myQuery+=param+","
	myQuery = myQuery[:-1] + ") VALUES (" #Quitar la última coma y preparar para los parámetros

	for value in values: #Agregar ellistado de valores
		try:
			value=myConnection.escape_string(value)#Evitar que nos hagan una inyección de sql
		except:
			print("no pude escapear el valor")
		myQuery+="'"+str(value)+"',"
	myQuery = myQuery[:-1] + ");" #Quitar la última coma y preparar para los parámetros
	
	#print(myQuery)
	cur.execute( myQuery )
	myConnection.commit()
	result=cur.fetchall()
	myConnection.close()
	if trace == True:
		print(str(result))
	return True #MEJORA ISSSUE 13

def doQuery( myQuery) :
	myConnection =pymysql.connect( host=hostname, user=username, passwd=password, db=database,charset='utf8' )	#Crear la conexión con la BD
	cur = myConnection.cursor()
	#myQuery = myConnection.escape_string(myQuery)
	cur.execute( myQuery )	
	result=cur.fetchall()
	myConnection.commit()
	myConnection.close()
	return result

def doTransaction(queriesList, traceback=False):
	print("Se iniciará la transacción...")
	try:
		myConnection =pymysql.connect( host=hostname, user=username, passwd=password, db=database,charset='utf8' )	#Crear la conexión con la BD
		cur = myConnection.cursor()
		a=0
		for query in queriesList:
			if traceback == True:
				print(query)
			cur.execute(query)
			a+=1
			if a%10000 == 0:
				print("Working in sentence number: "+str(a))
		print("Transacción armada.\nSe ejecutará...")
		myConnection.commit()
		myConnection.close()
		result=cur.fetchall()
		return "Transacción finalizada con éxito"
	except Exception as ex:
		print(ex)
		return "Error en la transacción"