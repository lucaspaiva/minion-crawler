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
method_type = "get"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
#Deptos en venta dueno
url_seed = "http://www.argenprop.com/Departamentos-Venta-Capital-Federal-Dueno-directo-Capital-Federal/mQ2KpQ1Kaf_800Kaf_816Kaf_100000001Kaf_500000001Kaf_700002102Kaf_600000135Kaf_1015KvnQVistaResultadosKvncQVistaGrilla"
#url_seed = "http://www.argenprop.com/Departamentos-Venta-Almagro-Capital-Federal/mQ2KpQ1Kaf_800Kaf_816Kaf_100000001Kaf_500000001Kaf_1015Kaf_800000002KvnQVistaResultadosKvncQVistaGrilla"

#TODO: Que son estos flags?
x = 1
n = 1
#---------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------------------
#BEGIN PROCESS
commons.print_f(">>>> INICIO PROCESO CRAWLING OLX")

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
    items = Parser.st_get_items(html_source,settings.xpath_query["ARPROP"]["item_list"])

    commons.print_f(">> Extraccion de datos ...")
    for index, item in enumerate(items):

        next_page = Parser.st_get_items(html_source,settings.xpath_query["ARPROP"]["next_page"])
        print next_page
        raw_input("hola")
        n+=1

        item = Parser(item)

        #extraigo datos
        title = item.parse(settings.xpath_query["ARPROP"]["item_title"])
        description = item.parse(settings.xpath_query["ARPROP"]["item_description"])
        price = item.parse(settings.xpath_query["ARPROP"]["item_price"])
        link = item.parse(settings.xpath_query["ARPROP"]["item_link"])
        link = "http://www.argenprop.com" + link
        r = Request(link,method_type,headers)
        html_source_detail = r.get_contents()
        #Convierto en objeto DOM con lxml
        item_detail = etree.HTML(html_source_detail)
        item_detail = Parser(item_detail)
        #phone = item_detail.parse(settings.xpath_query["ARPROP"]["item_phone"])
        phone = None
        location = item_detail.parse(settings.xpath_query["ARPROP"]["item_location"])
        sup = item_detail.parse(settings.xpath_query["ARPROP"]["item_sup"])
        amb = item_detail.parse(settings.xpath_query["ARPROP"]["item_amb"])


        if phone == None:
            phone = "No informa"
        if sup == None:
            sup = "No informa"
        if amb == None:
            amb = "No informa"
        if description == None:
            description = "No Informa"
        if price == None:
            price = "No Informa"            
        if title == None:
            title = "No Informa"     

        sup = sup.strip()
        amb = amb.strip()
        description = description.strip()

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

    next_page = Parser.st_get_items(html_source,settings.xpath_query["ARPROP"]["next_page"])  
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
file_name = "results_arprop_deptos_duenos.csv"
header_columns = [["Nro","Titulo","Descripcion","Precio","Localidad","Ambientes","Superficie","Telefono","Link"]]
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


