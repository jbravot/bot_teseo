#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Requires: Python >= 2.4
# Versions:
# bot_teseo.py 2.0
# Import

from BeautifulSoup import BeautifulSoup
import datetime, requests, json, csv, time

#--------------------------------------------------------------------
def write_csv(resultado, columnas, file_name):
    with open(file_name, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columnas)
        writer.writeheader()
        for data in resultado:
            writer.writerow(data)

# --------------------------------------------------------------------
def errorlogs(msg):
    f = open("error.txt", "a")
    f.writelines('**********************************************\n')
    f.writelines('FECHA: %s\n' % str(datetime.datetime.now()))
    f.writelines('ERROR: %s\n' % str(msg))
    f.writelines('**********************************************\n')
    f.close()

# --------------------------------------------------------------------
def write_file(csv_nombre):
    csvfile = open(csv_nombre, "a")
    writer = csv.DictWriter(csvfile, fieldnames=columnas, lineterminator='\n')
    writer.writeheader()
    csvfile.close()

# --------------------------------------------------------------------
def write_line(csv_nombre, line):
    csvfile = open(csv_nombre, "a")
    writer = csv.DictWriter(csvfile, fieldnames=columnas, lineterminator='\n')
    writer.writerow(line)
    csvfile.close()

#--------------------------------------------------------------------
def get_data_sublist(sublist):
    resultado = ""
    try:
        for li in sublist.find('ul').findAll('li', recursive=False):
            texto = limpiar_text(li.text)
            resultado = resultado + texto + ";"
    except Exception as e:
        errorlogs(" .-SUBLIST-. " + str(e))
    return resultado

#--------------------------------------------------------------------
def limpiar_text(texto):
    stop_words = ['&nbsp;', '\t', '\r', '\n', ',']

    for word in stop_words:
        texto = texto.replace(word, '')

    return texto.strip().encode("utf-8")

#--------------------------------------------------------------------
def scrap(obj_requests, columnas, indice):
    soup = BeautifulSoup(obj_requests.text)
    data = {}

    #obtenenos el contenido y limpiamos los datos
    div_contenido = soup.find('div', attrs={'id': 'contenido'})
    if div_contenido:
        try:

            #obtenemos el listado de datos
            li_list = div_contenido.find('ul').findAll('li', recursive=False)
            data = {'#':'', 'titulo':'', 'autor':'DESCONOCIDO', 'universidad':'DESCONOCIDO', 'departamento':'DESCONOCIDO',
                    'fecha':'', 'programa':'DESCONOCIDO', 'direccion':'DESCONOCIDO', 'tribunal':'DESCONOCIDO', 'descriptores':'DESCONOCIDO'}

            data['#'] = str(indice)
            for li in li_list:

                if 'T&iacute;tulo:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['titulo'] = limpiar_text(li.text)

                elif 'Autor:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['autor'] = limpiar_text(li.text)

                elif 'Universidad:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['universidad'] = limpiar_text(li.text)

                elif 'Departamento:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['departamento'] = limpiar_text(li.text)

                elif 'Fecha de Lectura:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['fecha'] = limpiar_text(li.text)

                elif 'Programa de doctorado:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['programa'] = limpiar_text(li.text)

                elif 'Direcci&oacute;n:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['direccion'] = get_data_sublist(li)

                elif 'Tribunal:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['tribunal'] = get_data_sublist(li)

                elif 'Descriptores:' in li.text.encode("utf-8"):
                    for tag in li.findAll('strong'):
                        tag.replaceWith('')
                    data['descriptores'] = get_data_sublist(li)

            print("%s - %s - %s" % (str(indice), data['titulo'], datetime.datetime.now()))

        except Exception as e:
            errorlogs(str(indice) + " .- " + str(e))
    else:
        print("%s - %s - %s" % (str(indice), "VACIO", datetime.datetime.now()))
        errorlogs(str(indice) + " .- " + "VACIO")

    return data

#--------------------------------------------------------------------
if __name__ == '__main__':

    resultado = []
    columnas = ['#','titulo', 'autor', 'universidad','departamento', 'fecha', 'programa', 'direccion', 'tribunal', 'descriptores']

    csv_nombre = 'resultados_%s.csv' % datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    write_file(csv_nombre)

    max_loop = 250
    num_loop = 1
    id_tesis_inicial = 3
    id_tesis_final = 172242

    for x in range(id_tesis_inicial,id_tesis_final,3):
        print("::::::::::::::::: TESIS NUMERO %s :::::::::::::::::" % x)

        try:
            obj_requests = requests.get('https://www.educacion.gob.es/teseo/mostrarRef.do?ref=' + str(x), verify=False)
        except Exception as e:
            print("******************** OCURRIO UN ERROR EN CONECCION DORMIRE 60 SEG")
            time.sleep(60)
            obj_requests = requests.get('https://www.educacion.gob.es/teseo/mostrarRef.do?ref=' + str(x), verify=False)

        tesis = scrap(obj_requests, columnas, x)
        if tesis:
            write_line(csv_nombre, tesis)

        if num_loop == max_loop:
            num_loop = 0
            time.sleep(5)
        num_loop = num_loop + 1
