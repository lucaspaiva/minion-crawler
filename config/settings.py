#---------------------------------------------------------------------------------------------------------------
## Archivo de configuracion general
#---------------------------------------------------------------------------------------------------------------
import os
import sys


#---------------------------------------------------------------------------------------------------------------
#SETEOS GENERICOS PARA LAS CONSULTAS XPATH
# config de expresiones xpath para parsear los datos necesarios, en caso de cambiar el layout
# cambiar el xpath solamente aca.
url_seeds = {}
xpath_query = {}

url_seeds["ML"] = {
					"ML"	 : "http://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/due%C3%B1o_DisplayType_LF_PrCategId_AD   ",
					"OLX"	 : "http://capitalfederal.olx.com.ar/nf/departamentos-casas-en-venta-cat-367/due%C3%B1o/-flo_apartaments"		
					}


xpath_query["ML"] = {
					"item_list"			: ".//li[@class='list-view-item rowItem']", #Listado de bloques div de items
					"item_title"		: ".//h3[@class='list-view-item-title']/a[1]/text()",
					"item_description"	: ".//p[@class='list-view-item-subtitle']/text()",
					"item_price"		: ".//span[@class='price-info-cost']/strong[@class='ch-price']/text()",
					"item_location"		: ".//li[@class='extra-info-location']/text()",
					"item_link"			: ".//h3[@class='list-view-item-title']/a/@href",
					"item_sup"			: ".//ul[@class='classified-details']/li[1]/text()",
					"item_amb"			: ".//ul[@class='classified-details']/li[2]/text()",
					"item_type_op"		: ".//ul[@class='classified-details']/li[3]/text()",
					"item_phone"		: ".//span[@class='seller-details-box showPhone']/text()",
					"next_page"			: ".//li[@class='last-child']/a/@href",
					} 


xpath_query["OLX"] = {
					"item_list"			: ".//ul[@class='items-list ']/li", #Listado de bloques div de items
					"item_title"		: ".//div[@class='items-info']/h3/text()",
					"item_description"	: ".//div[@class='items-info']/span/text()",
					"item_price"		: ".//p[@class='items-price']/text()",
					"item_location"		: ".//li[@class='icons icon-pin']/text()",
					"item_link"			: ".//a[@data-qa='list-item']/@href",
					"item_sup"			: ".//ul[@class='optionals']/li[contains(span,'Metros ')]/span[2]/text()",
					"item_amb"			: ".//ul[@class='optionals']/li[contains(span,'Dormitorios')]/span[2]/text()",
					"item_phone"		: ".//p[@class='icons icon-phone user-phone']/text()",
					"next_page"			: ".//a[@class='icons pagination-arrow icon-arrow-right ']/@href",
					}

xpath_query["ARPROP"] = {
					"item_list"			: ".//ul[@class='box-avisos-listado clearfix']/li[contains(@class,'avisoitem ')]", #Listado de bloques div de items
					"item_title"		: ".//h2[@class='address']/a/text()",
					"item_description"	: ".//p[@class='subtitle']/text()",
					"item_price"		: ".//p[@class='price']/text()",
					"item_location"		: ".//span[@class='callejero']/text()",
					"item_link"			: ".//h2[@class='address']/a/@href",
					"item_sup"			: ".//div[@class='detailItem' and contains(div,'sup. cubierta')]/div[@class='value']/text()",
					"item_amb"			: ".//div[@class='detailItem' and contains(div,'cant. dormitorios')]/div[@class='value']/text()",
					"item_phone"		: "", #en argenprop hay que estar logeado
					"next_page"			: ".//div[contains(a,'siguiente')]/a/@href",
					}			

xpath_query["INMCLA"] = {
					"item_list"			: ".//ul[@class='Items']/li[contains(@id,'liPreview_')]", #Listado de bloques div de items
					"item_title"		: ".//h3[@class='tituloaviso']/a/text()",
					"item_description"	: ".//li[@class='Tituloformat']/p/text()",
					"item_price"		: ".//p[@class='Money']/text()",
					"item_location"		: ".//span[@class='callejero']/text()",
					"item_link"			: ".//h3[@class='tituloaviso']/a/@href",
					"item_sup"			: ".//div[@class='detailItem' and contains(div,'sup. cubierta')]/div[@class='value']/text()",
					"item_amb"			: ".//div[@class='detailItem' and contains(div,'cant. dormitorios')]/div[@class='value']/text()",
					"item_phone"		: "", #en argenprop hay que estar logeado
					"next_page"			: ".//div[@class='siguiente']/a/@href",
					}

							 


#---------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------
#Database settings
db = {}
db["ec2_pro"] = {
				"host"		: "127.0.0.1",
				"port"		: 3306,
				"user"		: "root",
				"pass"		: "",
				"database"	: "mybd",
				"charset"	: "utf8"
				}
#---------------------------------------------------------------------------------------------------------------				


#---------------------------------------------------------------------------------------------------------------
#VARS
#Directorio donde se guardan los archivos CSV con el output del crawler
dir_path_csv = os.getcwd() + "/public/csvs"
dir_path_htmls = os.getcwd() + "/public/htmls"

#---------------------------------------------------------------------------------------------------------------

