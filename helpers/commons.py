#---------------------------------------------------------------------------------------------------------------
# HELPER COMMONS
# Name: commons.py
# Desc: Encapsula funciones estaticas utiles para el sistema
# Author: Lucas Paiva
#---------------------------------------------------------------------------------------------------------------

import datetime
import os
import csv
import os
import gzip
import glob
import sys
import unicodedata

def print_f(text):
	"""
	"""
	print str(datetime.datetime.now()) + ' - ' + text	

def generate_sql_insert(resultados,start,end):
    #global q
    #global resultados

    fechainsert=datetime.datetime.now()
    
    q="INSERT INTO paridad_booking_hoteles_dev (continente, pais, ciudad, dest_id, orden, checkin, checkout, hoteles_cantidad, \
    hoteles_disponibilidad, b_id, b_name, b_latitude, b_longitude, b_class, b_url, preciominimo, moneda, \
    max_persons, nombre_habitacion, cant_habitaciones, localidad, hotel_cercano, hotel_cercano_localidad, \
    oferta_inteligente, hotel_preferente, fechaobtencion, \
    fechainsert, cluster_id,  proceso_id, orden_checkin, tipo_tarifa ) VALUES  "
    
    for continente, pais, ciudad, dest_id, orden, \
        checkin, checkout, hoteles_cantidad, hoteles_disponibilidad, b_id, \
        b_name,  b_latitude, b_longitude, b_class, b_url, \
        preciominimo, moneda, max_persons, nombre_habitacion, cant_habitaciones, localidad, \
        hotel_cercano, hotel_cercano_localidad, oferta_inteligente, hotel_preferente, fechaobtencion, \
        cluster_id, proceso_id, orden_checkin, tipo_tarifa in resultados[start:end]:

        q=(q + "('%s', '%s', '%s', %s, %s, '%s', '%s', %s, %s, %s, '%s', %s, %s, '%s', '%s', %s, '%s', %s, '%s', %s ,'%s', %s, %s, %s, %s, '%s',\
                '%s', %s, %s, %s, '%s'), " %
                                (apostrofe(encutf_8(continente)),
                                apostrofe(encutf_8(pais)),
                                apostrofe(encutf_8(ciudad)),
                                encutf_8(dest_id),
                                encutf_8(orden),

                                apostrofe(encutf_8(checkin)),
                                apostrofe(encutf_8(checkout)),
                                apostrofe(encutf_8(hoteles_cantidad)),
                                apostrofe(encutf_8(hoteles_disponibilidad)),
                                apostrofe(encutf_8(b_id)),

                                apostrofe(encutf_8(b_name)),
                                apostrofe(encutf_8(b_latitude)),
                                apostrofe(encutf_8(b_longitude)),
                                encutf_8(b_class),
                                apostrofe(encutf_8(b_url)),

                                encutf_8(preciominimo),
                                apostrofe(encutf_8(moneda)),
                                encutf_8(max_persons),
                                apostrofe(encutf_8(nombre_habitacion)),
                                encutf_8(cant_habitaciones),
                                apostrofe(encutf_8(localidad)),
                                                            
                                encutf_8(hotel_cercano),
                                encutf_8(hotel_cercano_localidad),
                                encutf_8(oferta_inteligente),
                                encutf_8(hotel_preferente),
                                str(encutf_8(fechaobtencion)),

                                str(encutf_8(fechainsert)), #esta no viene de resultados
                                encutf_8(cluster_id), 
                                encutf_8(proceso_id),
                                encutf_8(orden_checkin),
                                apostrofe((tipo_tarifa))
                                 )).replace('None', 'NULL')

    return q

def get_directorios_htmls(path):
    """
    @Desc: Obtiene listado de directorios htmls a partir de un path

    @params:
    - path : string , ej: /home/lucas/ICHoteles/Projects/booking-crawler/htmls/2015-07-19

    @return: 
    - list[], ej: [['-597118', '2015-07-27'], ['-932338', '2015-08-10'], ['-932338', '2015-08-21']]
    """
    directorios_htmls = []

    try: 
        ciudades = os.listdir(path)
    except:
        ciudades = 0    

    if ciudades != 0:

        for dest_id in ciudades:
            dest_id = str(dest_id)
            checkins = os.listdir(os.path.join(path, dest_id))
            for checkin in checkins:
                directorios_htmls.append([dest_id, checkin])    
    else:

        directorios_htmls = 0                

    return directorios_htmls    

def read_html_from_gzip(path_file_name):
    """
    Desc: Levanta y descomprime un archivo gzip y devuelve en texto plano

    Params:
    - path_file_name : string

    return:
    - html : string
    """
    f = gzip.open(path_file_name, 'rb')
    html = f.read()
    f.close()
    #Decodea html del archivo en cuestion.
    html = decutf_8(html)
    return html

def get_csv_content(path_file_name):
    """
    Desc: obtiene datos del csv y retorna una lista con los valores esperados

    Params:
    - path_file_name : string
    
    return:
    - [] : list
    """
    datoscsv = []

    archivocsv = path_file_name.replace('html.gz', 'html.csv')

    with open(archivocsv, 'rb') as f:
        reader = csv.reader(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in reader:
            datoscsv.append(row)
            
    dest_id, continente, pais, ciudad, moneda, hoteles_esperados, fecha_ejecucion, checkin, orden_checkin, los, pax, cluster_id, pagina, proceso_id = datoscsv[0]
    continente = decutf_8(continente)
    pais = decutf_8(pais)
    ciudad = decutf_8(ciudad)
    dest_id = decutf_8(dest_id)
    orden_checkin = decutf_8(orden_checkin)
    if orden_checkin == '':
        orden_checkin='NULL'
    los = int(los)
    cluster_id=decutf_8(cluster_id)
    checkin = datetime.datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
    checkout = checkin + datetime.timedelta(days=los)
    proceso_id=decutf_8(proceso_id)

    return [dest_id, continente, pais, ciudad, moneda, hoteles_esperados, fecha_ejecucion, checkin, checkout, orden_checkin, los, pax, cluster_id, pagina, proceso_id]

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def creacarpeta(s):
    if not os.path.isdir(s):
        os.mkdir(s)
    return

#TODO: Funcion trambolica, reeplazar
def extrae_texto(texto, texto_ini, texto_fin):
    if texto.find(texto_ini) >= 0 :
        ini = texto.find(texto_ini)+len(texto_ini)
        if texto.find(texto_fin,ini) >= 0:
            fin = texto.find(texto_fin,ini)
            return texto[ini:fin]
    return None

def decutf_8(str):
    try:
        return str.decode('utf-8')
    except:
        return str

def encutf_8(str):
    try:
        return str.encode('utf-8')
    except:
        return str

def apostrofe(s):
    try:
        ret = s.replace("'", "")
    except:
        ret = s
    return ret

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

def limpieza_barras_por_espacios(x):
    x= x.replace('\r', '\n')
    x= x.replace('\t', '\n')
    x = x.replace('\n ', '\n')
    x= x.replace(' \n', '\n')
    while x.find('\n \n') >= 0:
        x = x.replace('\n \n', '\n')
    while x.find('\n\n') >= 0:
        x = x.replace('\n\n', '\n')
    x = x.replace('\n', ' ')
    while x.find('  ') >= 0:
        x = x.replace('  ', ' ')
    return x
