#---------------------------------------------------------------------------------------------------------------
# Name: Proyecto Bookig Crawler
# Desc: Parser booking basado en la version anterior (Crawler_Booking_HTMLS_to_DB_V6.0) , 
#       completamente refactoreado, aplicacion de principios de diseno y reutilizacion de codigo.
# Estructura de la aplicacion:
# -
#---------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------
#LIBS, HELPERS, MODULES, VARS
#Respetando PEP8, primero modulos de python, luego de terceros y finalmente propios.
#Nativos
import os
import datetime
import sys

#Terceros
import glob
from lxml import etree
import lxml.html

#Propios
from classes.connection import Connection
from classes.parser import Parser
from classes.request import Request
import helpers.commons as commons
import helpers.cleaner as cleaner
import config.settings as settings
#from helpers.mail import *

#VARS
#resultados = []
#id_hoteles = []
#contador para el orden
#contador = 1
#Para insert x lotes
#start=0
#end=100

articles = []
method_type = "post"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/due%C3%B1o_DisplayType_LF_PrCategId_AD"

#TODO: Que son estos flags?
x = 1
n = 1
#---------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------
#BEGIN PROCESS
commons.print_f(">>>> INICIO PROCESO CRAWLING")

#Proceso de Crawling
while True:
    commons.print_f(">> Pagina: " + str(x) )
    commons.print_f(">> Ejecuto request ...")
    
    #TODO: Esto es lo mismo que hacer el if y cambiar la url que llamar dos veces a Request.
    if x == 1:
        r = Request(url_seed,method_type,headers)
    else:
        r = Request(next_page,method_type,headers)  

    #Envio peticion y obtengo contenido
    status = r.get_status_response()
    html_source = r.get_contents()
    #Convierto en objeto DOM con lxml
    #html = etree.HTML(html_source)

    #Aca ejecuto el crawling de la pagina
    ##################################################
    #Comienzo el parseo, extraigo el html del listado 
    #items = html.xpath(".//li[@class='list-view-item rowItem']")
    items = Parser.st_get_items(html_source,settings.xpath_query["item_list"])

    commons.print_f(">> Extraccion de datos ...")
    for index, item in enumerate(items):
        n+=1

        item = Parser(item)

        #extraigo datos
        title = item.parse(settings.xpath_query["item_title"])
        description = item.parse(settings.xpath_query["item_description"])
        price = item.parse(settings.xpath_query["item_price"])
        location = item.parse(settings.xpath_query["item_location"])
        link = item.parse(settings.xpath_query["item_link"])
        sup = item.parse(settings.xpath_query["item_sup"])
        amb = item.parse(settings.xpath_query["item_amb"])
        
        #navego link de detalle de inmueble para extraer el telefono
        link_with_phone = link + "?noIndex=true&showPhones=true"
        r = Request(link_with_phone,method_type,headers)
        html_source_detail = r.get_contents()
        #Convierto en objeto DOM con lxml
        item_detail = etree.HTML(html_source_detail)
        item_detail = Parser(item_detail)
        phone = item_detail.parse(settings.xpath_query["item_phone"])

        if phone == None:
            phone = "No informa"

        commons.print_f(">> Item n: " + str(n) )
        commons.print_f(">> URL: " + link )    
        commons.print_f(">> Titulo: " + title)
        commons.print_f(">> Descripcion: " + description)
        commons.print_f(">> Precio: " + price)
        commons.print_f(">> Zona: " + location)
        commons.print_f(">> Superficie: " + sup)
        commons.print_f(">> Ambientes: " + amb)
        commons.print_f(">> Telefono: " + str(phone) )   
        commons.print_f(">>")    

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

    next_page = Parser.st_get_items(html_source,settings.xpath_query["next_page"])  
    next_page = next_page[0]
    
    commons.print_f(">> Proxima pagina: ")    
    commons.print_f(">> " + next_page)    
    commons.print_f(">> ")    
    commons.print_f(">> ")    

    x += 1

    #Si no hay mas paginas viene en None, entonces salgo
    if next_page == None:   
        last_page = True
        commons.print_f(">> Fin paginacion")    
    else:
        last_page = False

    if last_page:
        break


print " "
print "> Grabo archivo"   
f= open('results_ml_deptos_duenos.csv', 'wb')   
file = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
header_columns = [["Nro","Titulo","Descripcion","Precio","Localidad","Ambientes","Superficie","Telefono","Link"]]
file.writerows(header_columns)
file.writerows(articles)
f.close()        

#END PROCESS
#---------------------------------------------------------------------------------------------------------------




           

#---------------------------------------------------------------------------------------------------------------
#INSERTO EN BASE DE DATOS

"""
commons.print_f(">> Inserta en base de datos")

conn = Connection(settings.db["ec2_pro"])

l = len(resultados)

if l==0:
    commons.print_f(">> No hay datos para insertar")
else:

    while end <= l:
    
        q = commons.generate_sql_insert(resultados,start,end)

        q=q[:len(q)-2]
        conn.execute_query(q)
        start=start+100
        end=end+100
        commons.print_f(">> Inserto lote - Start: " + str(start) + " , End: " + str(end) )

    
    if end >l:
    
        q = commons.generate_sql_insert(resultados,start,end)

        q=q[:len(q)-2]
        conn.execute_query(q)
        commons.print_f(">> Inserto ultimo lote...")
"""        
#FIN - INSERTO EN BASE DE DATOS
#---------------------------------------------------------------------------------------------------------------


