import requests
#import urllib2
#import simplejson
import sys
import time
#from helper import send_mail
#mport settings

class Request:
	#ATTRIBUTES

	#Pagina inicial: 
	url_first_page = ""
	#Pagina inicial paginado (JSON): 	
	url_first_page_paging = ""
	content_type = "html"
	headers = {}
	method_type = "get"

	__timeout__ = 10 #Float segundos para que genere timout
	__max_retry__ = 4 #cantidad de intentos
	__seconds__ = 20 #segundos de espera antes de nuevo intento de request

	result_json = {}
	error = []

	#Constructor:
	def __init__(self,url,method,headers={}):
		self.url_first_page = url
		self.method_type = method
		self.headers = headers

	def get_contents(self,retrys=1):
		"""
		Realiza request y devuelve contenido
		Metodo recursivo
		return string
		"""
		
		try:

			if self.method_type == "get":
				r = requests.get(self.url_first_page, headers=self.headers, timeout=self.__timeout__)
			elif self.method_type == "post":
				r = requests.post(self.url_first_page, headers=self.headers, timeout=self.__timeout__)

			ret = r.content

			if len(r.content) == 0:
				#TODO: Si esta vacio es porque algo anda mal, tambien habria que guardarlo en un log de errores para un futuro procesamiento.
				print "Devuelve contenido vacio"	

			return ret	

		except requests.exceptions.Timeout:
			if retrys < self.__max_retry__:
				print "Timeout - intento ",retrys," Esperando ",self.__seconds__," segundos..."
				time.sleep(self.__seconds__)
				retrys = retrys + 1
				self.get_contents(retrys)
			else:
				print "Error general"	
				print "Intentos: ", retrys
				print "No sepuede continuar con el proceso - Fin intentos "
				#sys.exit()


		except requests.exceptions.RequestException as e:
			return "Error desconocido: ", e	

	#FIN get_contents()		


	def get_status_response(self):
		#Realiza request y devuelve esatdo (header y status)
		#return dic
		#TODO: Controlar el tiempo de timeout
		r = requests.get(self.url_first_page)
		status = {
			"code": r.status_code,
			"headers": r.headers
			}
		return status

	def get_json_contents(self,id_ciudad,retrys=1):
		#TODO: Refactorear toda esta cumbia

		#flag de contenido correcto
		content_ok = 0
		content_empty = 0
		flagErrorContent = 0

		try:
			r = requests.post(self.url_first_page, timeout=self.__timeout__)
			try:
				ret = r.json()
			except UnboundLocalError:
				# simplejson.scanner.JSONDecodeError
				print "Fallo el metodo recursivo, continuo"	
				print "Contenido: ", ret
				print "Longitud contenido: ", len(ret) 
				subject = "Error HU Robot" 
				email_content =  """Hubo un error, Fallo el metodo para obtener el json. 
				Error al procesar la ciudad: %s .
				Contenido del resultado que origino else error: 
				%s """ % (str(id_ciudad), str(r))
				#asigno none a ret
				flagErrorContent = 1

			except simplejson.scanner.JSONDecodeError:	
				print "Fallo el metodo al obtener JSON"	
				#TODO: Lo comento porque aparentemente no devuelve nada en ret
				#print "Contenido: ", ret
				#print "Longitud contenido: ", len(ret) 
				subject = "Error HU Robot" 
				email_content =  """Hubo un error, Fallo el metodo para obtener el json. <br> 
				Error al procesar la ciudad: %s . <br>
				Contenido del resultado que origino el error: <br>
				%s <br>
				Tipo de error: simplejson.scanner.JSONDecodeError """ % (str(id_ciudad), str(r))
				#asigno none a ret
				flagErrorContent = 1
				#Le asigno vacio para que no putie
				ret = {}

			#TODO: Esto se podria refactorear
			if ret.has_key("searching"):
			#Entra por aca si el json que devuelve no es valido 

				print "El resultado es buscando... : "
				print ret
				
				if retrys < self.__max_retry__:
					print " "
					print "Sin contenido - intento ",retrys," Esperando ",self.__seconds__," segundos..."
					time.sleep(self.__seconds__)
					retrys = retrys + 1
					#TODO: Revisar si este manejo de error esta bien
					#self.get_json_contents(retrys)
					self.get_json_contents(id_ciudad,retrys)
				else:
					print "Imposible obtener contenido."	
					print "Intentos: ", retrys
					print "No sepuede continuar con el proceso - Fin intentos "
					"""
					TODO: Aqui habria que crear una lista con los errores, para luego volver a procesarlos . 
					"""
					subject = "Error HU Robot" 
					email_content =  """Hubo un error. 
					No se pudo obtener resultados de la ciudad: %s """ % (str(id_ciudad))
					send_mail(settings.send_from, settings.send_to, subject, email_content)
					#Le aisgno none para que no corte en el py del robot
					self.result_json = None
										
			else:
				content_ok = 1	

			#TODO: Revisar esta cumbia	
			if flagErrorContent == 1:
				self.result_json = None	
				content_ok = 0

			if ret.has_key("empty"):
				content_empty = 1

			if content_empty == 1:		
				self.result_json = None
				
			if content_ok == 1 and content_empty == 0:		
				self.result_json = ret
				#return ret
		
		except requests.exceptions.Timeout:
			#print "Time out "
			if retrys < self.__max_retry__:
				print "Timeout - intento ",retrys," Esperando ",self.__seconds__," segundos..."
				time.sleep(self.__seconds__)
				retrys = retrys + 1
				self.get_contents(retrys)
			else:
				print "Error general"	
				print "Intentos: ", retrys
				print "No sepuede continuar con el proceso - Fin intentos "

				subject = "Error HU Robot" 
				email_content =  """Hubo un error de timout. 
				No se pudo obtener resultados de la ciudad: %s """ % (str(id_ciudad))

		except requests.exceptions.RequestException as e:
			print "Error desconocido: ", e	

		#FIN get_json_contents()

	def get_json_result(self):
		"""
		Devuelve el resultado del json
		TODO: Validar si result_json esta conmpleto sino devolver otra cosa (a definir)
		"""
		return self.result_json	