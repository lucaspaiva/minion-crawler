import MySQLdb
import sys

__author__ = "Lucas Paiva"
__description__ = "Clasesita simple para trabajar con mysql. be happy ;) "

class Connection(object):
	__host = None
	__port = None
	__user = None
	__pass = None
	__database = None
	__charset = None

	__connection = None
	__cursor = None


	def __init__(self,dic_params={}):
		"""
		Contructor

		Params:
		- dic_params (DIC) : recibe un diccionario con los datos de conexion
		"""
		self.__host = dic_params["host"]
		self.__port = int(dic_params["port"])
		self.__user = dic_params["user"]
		self.__pass = dic_params["pass"]
		self.__database = dic_params["database"]
		self.__charset = dic_params["charset"]

	def _open_connection(self):
		"""
		Metodo privado que abre conexion
		"""
		try:
			cn = MySQLdb.connect(host=self.__host, port=self.__port, user=self.__user, passwd=self.__pass, db=self.__database, charset=self.__charset)
			self.__connection = cn
			self.__cursor = cn.cursor()
		except:
			print "Se produjo un error al conectar con el servidor de base de datos."	
			
	def _close_connection(self):
		"""
		Metodo privado que cierra conexion
		"""
		self.__cursor.close()
		self.__connection.close()

	def	get_results_query(self,str_query):
		"""
		Metodo que devuelve un resultset de una consulta

		Params:
		- str_query (STR) : consulta sql.

		Return:
		- result (resulset).
		"""
		result = None
		self._open_connection()
		self.__cursor.execute(str_query)
		result = self.__cursor.fetchall()
		self._close_connection()
		return result

	def execute_query(self,str_query):
		"""
		Metodo que ejecuta una operacion sobre la BD (Delete, Update, Insert)
		* Tmb se puede usar para ejecutar un store procedure ;) 

		Params:
		- str_query (STR) : consulta sql.		
		"""
		self._open_connection()
		self.__cursor.execute(str_query)
		self.__connection.commit()
		self._close_connection()	

	def call_store_proc(self,proc,*args):
		"""
		Metodo que ejecuta un store procedure, recibe una lista de argumentos opcionales

		Params:
		- proc (STR) : nombre del store
		- args (LIST) : lista de n argumentos.

		Result:
		- result_sp : resultset

		Implementacion (ej.):
		args = ['param1',1,15]
		r = objInstance.call_store_proc("sp_cualquiera",args) 

		"""
		result_sp = None
		self._open_connection()
		self.__cursor.callproc(proc, args)
		self.__connection.commit()
		for result in self.__cursor.stored_results():
			result_sp = result.fetchall()
		self._close_connection()
		return result_sp

	def insert(self, table, **kwargs):
		"""
		Metodo generico que inserta datos.
		TODO: Probar el metodo con campos string con caracteres especiales

		Params:
		- table (str) : Nombre de la tabla
		- **kwargs (key:value) : Lista de argumentos clave=valor .

		Return:
		- lastrowid : Ultimo ID generado

		Ej: Implementacion:

		conn.insert(table='cronograma_ejecucion',
			fecha_ejecucion='2015-05-21',
			id_informe=1,
			id_sitio=1) 

		"""
		values = None
		query = "INSERT INTO %s " % table

		if kwargs:
			keys = kwargs.keys()
			values = kwargs.values()
			query += "(" + ",".join(["`%s`"]*len(keys)) % tuple(keys) + ") VALUES(" + ",".join(["%s"]*len(values)) + ")"

		self._open_connection()
		self.__cursor.execute(query, values)
		self.__connection.commit()
		self._close_connection()
		return self.__cursor.lastrowid		

	




	


						


		
