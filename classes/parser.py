#---------------------------------------------------------------------------------------------------------------
# Description: Clase adhoc para parsear datos de hoteles en un resultado de busqueda de booking
# Author: Lucas Paiva
#---------------------------------------------------------------------------------------------------------------

from lxml import etree

#---------------------------------------------------------------------------------------------------------------
#Class

#TODO: La mejor practica es crear un super clase (abstracta o no) que sea Parser y BookingParser que extienda de esa superclase
class Parser(object):

	__html = None

	def __init__(self,html):
		"""
		Contructor
		Params:
 		"""
		self.__html = html

	#---------------------------------------------------------------------------------------------------------------
	#Public methods

	def parse(self,exp):
		"""
		Description: Metodo generico que parsea html y devuelve string, notar que este metodo define un parseadeor
		generico, en la implementacion se decide que metodo usar (xpath, expresiones regulares, etc), y
		eventualmente con que modulo realizarlo si con lxml, beatifulsoup, etc.

		Params:
		- exp (str) : expresion a buscar (xpath generalmente, pero podria implementarse otra cosa)

		Return:
		- str
		"""
		return self._parse_by_xpath(exp)


	#END - Public methods	
	#---------------------------------------------------------------------------------------------------------------



	#---------------------------------------------------------------------------------------------------------------
	#Private methods

	def _parse_by_xpath(self,xpath_exp):	
		"""
		"""
		r = self.__html.xpath(xpath_exp)
		if len(r)>0:
			r = r[0]
		else:
			r = None	

		return r

	#Private methods
	#---------------------------------------------------------------------------------------------------------------



	#---------------------------------------------------------------------------------------------------------------
	#Private methods

	@staticmethod
	def st_get_items(html,xpath_exp):
		"""
		TODO: Refactorear esto, para usar metodos de helpers o algo asi.
		"""
		html = etree.HTML(html)
		items = html.xpath(xpath_exp)
		return items

	#Private methods	
	#---------------------------------------------------------------------------------------------------------------

		

#End Class	
#---------------------------------------------------------------------------------------------------------------