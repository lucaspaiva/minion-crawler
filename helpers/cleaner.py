#---------------------------------------------------------------------------------------------------------------
# HELPER CLEANER
# Name: cleaner.py
# Desc: Encapsula funciones estaticas para formatear y limpiar el output del parser
# Author: Lucas Paiva
#---------------------------------------------------------------------------------------------------------------
import helpers.commons as commons
import sys
import re
import HTMLParser

def clean_hotel_id(string):
	"""
	"""
	r = string.replace("hotel_","")
	return r 

def clean_hotel_name(string):
	"""
	"""
	r = string.strip()
	return r 	

def clean_hotel_latitude(string):
	"""
	"""
	r = string.split(",")
	r = r[0]
	return r

def clean_hotel_longitude(string):
	"""
	"""
	r = string.split(",")
	r = r[1]
	return r

def clean_hotel_category_stars(string):
	"""
	"""
	if string is not None:
		r = string.replace("b-sprite stars ratings_stars_","")
		r = r.replace("star_track","")
		r = r.strip()
	else:
		r = 0

	return r		

def clean_hotel_url(string):
	"""
	"""
	r = string[: string.find('?')]
	return r

def clean_hotel_price(string):
	"""
	"""
	if string is not None:
		r = string.replace('.', '')
		r = r.replace(',', '.')
		#extraigo solo numeros con expresion regular en vez de mil replace ;)
		r = str(re.findall('\d+', r)[0])
		if commons.is_number(r):
			r = float(r)
	else:
		r = 0

	return r		

def clean_hotel_maxpersons(string):
	"""
	"""
	if string is not None:
		r = int(re.findall('\d+', string)[0])
	else:
		r = 0

	return r

def clean_hotel_room_name(string):
	"""
	"""
	if string is not None:
		r = string.strip()
	else:
		r = "-"

	return r
	
def clean_hotel_location(string):
	"""
	"""
	if string is not None:
		r = HTMLParser.HTMLParser().unescape(string)
		r = commons.limpieza_barras_por_espacios(r)
		if r.find('(') >= 0:
			r = r[:r.find('(')]
		if r.find('&bull;') >= 0:
			r = r[:r.find('&bull;')]
		if r.find('Chatl') >= 0:
			r='El Chalten'
			r=decutf_8(r)
		if r.find("Arraial d'Ajuda") >= 0:
			r="Arraial d' Ajuda"
			r=decutf_8(r)
		if r.find("achupicchu") >= 0:
			r="Machu Picchu"
			r=decutf_8(r)
		if r.find("Ilha Bela") >= 0:
			r="Ilhabela"
			r=decutf_8(r)
	else:
		r = "-"

	return r

def clean_hotel_smart_deal(string):
		"""
		"""	
		if string is not None:
			r = 1
		else:
			r = 0

		return r		

def clean_hotel_prefer(string):	
	"""
	Cambie por esta condicion porque me tiraba un warning si hacia solo if hotel_preferente:
	"""
	if string is not None: 
		r = 1
	else:
		r = 0

	return r							
