#---------------------------------------------------------------------------------------------------------------
## Archivo de configuracion general
#---------------------------------------------------------------------------------------------------------------
import os
import sys

#---------------------------------------------------------------------------------------------------------------
#SETEOS GENERICOS PARA LAS CONSULTAS XPATH
# config de expresiones xpath para parsear los datos necesarios, en caso de cambiar el layout
# cambiar el xpath solamente aca.

xpath_query = {
			"item_list"			: ".//li[@class='list-view-item rowItem']", #Listado de bloques div de items
			"item_title"		: ".//h3[@class='list-view-item-title']/a[1]/text()",
			"item_description"	: ".//p[@class='list-view-item-subtitle']/text()",
			"item_price"		: ".//span[@class='price-info-cost']/strong[@class='ch-price']/text()",
			"item_location"		: ".//li[@class='extra-info-location']/text()",
			"item_link"			: ".//h3[@class='list-view-item-title']/a/@href",
			"item_sup"			: ".//ul[@class='classified-details']/li[1]/text()",
			"item_amb"			: ".//ul[@class='classified-details']/li[2]/text()",
			"item_phone"		: ".//span[@class='seller-details-box showPhone']/text()",
			"next_page"			: ".//li[@class='last-child']/a/@href",
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


#---------------------------------------------------------------------------------------------------------------

