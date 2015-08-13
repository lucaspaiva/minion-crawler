"""
Crawler para mercadolibre inmuebles
TODO: aca deberia crear una carpeta classes para poner mi clase request e importarla como modulo
"""
#Librerias sistema
from lxml import etree
import lxml.html
import sys
import os
import csv
#Libs, clases propias
from classes.request import Request
#Vars
articles = []
method_type = "post"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}

print "############ Crawling simple para ML ##############"

#Departamentos en venta de dueno
#url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/due%C3%B1o_DisplayType_LF_PrCategId_AD"
#Departamentos en venta dueno capital federal
url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/due%C3%B1o_DisplayType_LF_PrCategId_AD"
print "URL Seed: "
print url_seed
print " "

x = 1
n = 1

while True:

	print "> Pagina: ", x
	print "> Ejecuto request ..."
	
	#TODO: Esto es lo mismo que hacer el if y cambiar la url que llamar dos veces a Request.
	if x == 1:
		r = Request(url_seed,method_type,headers)
	else:
		r = Request(next_page,method_type,headers)	



	#Envio peticion y obtengo contenido
	status = r.get_status_response()
	html_source = r.get_contents()
	#Convierto en objeto DOM con lxml
	html = etree.HTML(html_source)

	#Aca ejecuto el crawling de la pagina
	##################################################
	#Comienzo el parseo, extraigo el html del listado 
	items = html.xpath(".//li[@class='list-view-item rowItem']")

	print "> Extraccion de datos ..."
	for index, item in enumerate(items):
		n+=1
		#extraigo datos
		title = item.xpath(".//h3[@class='list-view-item-title']/a[1]/text()")
		title = title[0]
		description = item.xpath(".//p[@class='list-view-item-subtitle']/text()")
		description = description[0]
		price = item.xpath(".//span[@class='price-info-cost']/strong[@class='ch-price']/text()")
		price = price[0]
		location = item.xpath(".//li[@class='extra-info-location']/text()")
		location = location[0]
		link = item.xpath(".//h3[@class='list-view-item-title']/a/@href")
		link = link[0]
		sup = item.xpath(".//ul[@class='classified-details']/li[1]/text()")
		sup = sup[0]
		amb = item.xpath(".//ul[@class='classified-details']/li[2]/text()")
		amb	= amb[0]

		#navego link de detalle de inmueble para extraer el telefono
		link_with_phone = link + "?noIndex=true&showPhones=true"
		print ">> Item n: ", index
		print ">> Titulo: ", title
		print ">> Descripcion: ", description
		print ">> Precio: ", price
		print ">> Zona: ", location
		print ">> Superficie: ", sup
		print ">> Ambientes: ", amb

		print "## Request a pagina detalle ..."
		r = Request(link_with_phone,method_type,headers)
		html_source_detail = r.get_contents()
		#Convierto en objeto DOM con lxml
		html_detail = etree.HTML(html_source_detail)
		if html_detail.xpath(".//span[@class='seller-details-box showPhone']/text()"):
			phone = html_detail.xpath(".//span[@class='seller-details-box showPhone']/text()")
			phone = phone[0]
		else:
			phone = "No informa"	
		print ">> Telefono: ", phone
		print " "

		#Agrego a la lista de avisos
		articles.append([n, 
						title.encode("utf-8"), 
						description.encode("utf-8"), 
						price.encode("utf-8"),
						location.encode("utf-8"),
						amb.encode("utf-8"),
						sup.encode("utf-8"),
						phone.encode("utf-8"),
						link.encode("utf-8")
						])

	##################################################

	if html.xpath(".//li[@class='last-child']/a/@href"):
		next_page = html.xpath(".//li[@class='last-child']/a/@href")
		next_page = next_page[0]
	else:
		next_page = None

	print "> Proxima pagina: "
	print next_page
	print " "
	print " "

	x += 1

	#Si no hay mas paginas viene en None, entonces salgo
	if next_page == None:	
		last_page = True
		print "Fin paginacion"
	else:
		last_page = False

	if last_page:
		break

#grab archivo
print " "
print "> Grabo archivo"   
f= open('results_ml_deptos_duenos.csv', 'wb')   
file = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
header_columns = [["Nro","Titulo","Descripcion","Precio","Localidad","Ambientes","Superficie","Telefono","Link"]]
file.writerows(header_columns)
file.writerows(articles)
f.close()








#print html
