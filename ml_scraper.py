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
import csv

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
file_name = "2015-09-23_ml_veraneo_duenos.csv"
method_type = "post"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
#url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/due%C3%B1o_DisplayType_LF_PrCategId_AD   "
#url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/due%C3%B1o_DisplayType_LF_ItemTypeID_N_PrCategId_AD "
#Todo departamentos en venta:
#url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/due%C3%B1o_DisplayType_LF_PrCategId_AD "
#Todo casas de dueno en venta:
#url_seed = "http://inmuebles.mercadolibre.com.ar/casas/due%C3%B1o_DisplayType_LF"
#Todo alquiler temporario de dueno:
url_seed = "http://inmuebles.mercadolibre.com.ar/alquiler-temporario/due%C3%B1o_DisplayType_LF"




#TODO: Que son estos flags?
x = 1
# nro de orden
n = 0
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
    #print "html dom: "
    #print html_source
    #print "Grabo archivo"   
    #archivo = open('public/htmls/pagina1.html', 'wb')   
    #archivo.write(html_source)
    #archivo.close()
    #sys.exit()

    #Aca ejecuto el crawling de la pagina
    ##################################################
    #Comienzo el parseo, extraigo el html del listado 
    #items = html.xpath(".//li[@class='list-view-item rowItem']")
    items = Parser.st_get_items(html_source,settings.xpath_query["ML"]["item_list"])
    #print "Items: ", items
    #raw_input("Siguiente")

    commons.print_f(">> Extraccion de datos ...")
    for index, item in enumerate(items):
        n+=1

        item = Parser(item)

        #extraigo datos
        title = item.parse(settings.xpath_query["ML"]["item_title"])
        description = item.parse(settings.xpath_query["ML"]["item_description"])
        price = item.parse(settings.xpath_query["ML"]["item_price"])
        location = item.parse(settings.xpath_query["ML"]["item_location"])
        link = item.parse(settings.xpath_query["ML"]["item_link"])
        sup = item.parse(settings.xpath_query["ML"]["item_sup"])
        amb = item.parse(settings.xpath_query["ML"]["item_amb"])
        operation = item.parse(settings.xpath_query["ML"]["item_type_op"])
        

        title = cleaner.clean_spaces(title)
        description = cleaner.clean_spaces(description)
        location = cleaner.clean_spaces(location)
        
        #navego link de detalle de inmueble para extraer el telefono
        link_with_phone = link + "?noIndex=true&showPhones=true"
        r = Request(link_with_phone,method_type,headers)
        html_source_detail = r.get_contents()
        #Convierto en objeto DOM con lxml
        if html_source_detail != "":
            item_detail = etree.HTML(html_source_detail)
            item_detail = Parser(item_detail)
            phone = item_detail.parse(settings.xpath_query["ML"]["item_phone"])
        else:
            phone = "Error en request"    

        #Validaciones extra
        if phone == None:
            phone = "No informa"

        if operation == None:
            operation = "Ver columna amb."    

        if amb == None:
            amb = "-"    

        commons.print_f(">> Item n: " + str(n) )
        commons.print_f(">> URL: " + link )    
        commons.print_f(">> Titulo: " + title)
        commons.print_f(">> Descripcion: " + description)
        commons.print_f(">> Precio: " + price)
        commons.print_f(">> Tipo de operacion: " + operation)
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
                        operation.encode("utf-8"),
                        phone.encode("utf-8"),
                        link.encode("utf-8")
                        ])

    ##################################################

    next_page = Parser.st_get_items(html_source,settings.xpath_query["ML"]["next_page"])  
    if len(next_page) != 0:
        next_page = next_page[0]
    else:    
        next_page = 0

    x += 1

    #Si no hay mas paginas viene en None, entonces salgo
    if next_page == 0:   
        last_page = True
        commons.print_f(">> Fin paginacion")    
    else:
        last_page = False

    if last_page:
        break

    commons.print_f(">> Proxima pagina: ")    
    commons.print_f(">> " + next_page)    
    commons.print_f(">> ")    
    commons.print_f(">> ")    


commons.print_f(" ")
commons.print_f("> Grabo archivo")   
header_columns = [["Nro","Titulo","Descripcion","Precio","Localidad","Ambientes","Superficie","Tipo Operacion","Telefono","Link"]]
commons.save_csv(settings.dir_path_csv,file_name,articles,header_columns)

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


