# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error

palabras_sobrantes = ["de","que","un","una","unos","unas","el","la","los","las","es","son","a","del","se","le","o","u","su","en","como","cuando","y","si", "cual","para","ha","cada","donde"]

palabras_fijas=["entidad","relación","atributo","diagrama","crear","editar","eliminar","juntar","separar"]

texto = "Una beca es una ayuda económica que proviene de fondos públicos, la cual se concede a una persona para pagar de forma total o parcial los gastos que le supone cursar estudios académicos, desarrollar un proyecto de investigación o realizar una obra artística. Se desea crear un sistema que realice el seguimiento de los desembolsos que se realizan a las personas."

pistas=["Se desea registrar la siguiente información sobre la persona que recibe la beca: nombres, apellidos, numero de cédula de identidad o pasaporte, dirección, teléfono, correo electrónico, ciudad de nacimiento, ciudad de residencia, títulos académicos que posee, nombre y país de la institución de donde obtuvo el título académico, nivel de instrucción (e.j: bachillerato, 3er nivel o 4to nivel), fecha de obtención del título","Además se desea guardar la información de todos los trabajos que ha tenido en los últimos 8 años indicando el nombre de la empresa o institución, si es pública o privada, fecha de ingreso, fecha de salida si fuese el caso, cargo y descripción de la actividad que realiza.","Una beca tiene una fecha de inicio, fecha fin, presupuesto (en dólares), un estado (pre-aprobada, aprobada, en ejecución, finalizada). See desea también registrar el saldo que se le adeuda a la persona durante el transcurso de la beca, así como también registrar cuántos depósitos se han realizado hasta el momento. Luego de finalizada la beca se procede a liquidar los valores o se procede a dar una prórroga.","La beca da lugar a varios desembolsos realizados a la cuenta de la persona que recibe la beca. Para cada desembolso de desea guardar la siguiente información: fecha de desembolso, país, moneda (USD, EUR, AUD, etc). monto, numero de cuenta, nombre del banco, código SWIFT.","Una vez realizado el desembolso, se le pide a la persona que recibe el dinero que envíe una copia del comprobante de depósito para que sea guardado como registro en la base de datos.","Una persona puede recibir varias becas durante su existencia."]

filas=[]

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def obtener_sesiones(conn):
	cur = conn.cursor()
	cur.execute("select sesion,estudiante,texto from Interaccions where (sesion=281 or sesion=284 or sesion=286 or sesion=300 or sesion=293 or sesion=297 or sesion=307 or sesion=309) and tipo_interaccion='TRANSCRIPT'")
	rows = cur.fetchall()
	for row in rows:
		filas.append(row)


def quitar_palabras_sobrantes(texto):
	arreglo = texto.split()
	arreglo2 = []
	for i in range(0,len(arreglo)):
		arreglo[i]=arreglo[i].lower().strip('()-,.:')
		if es_palabra_sobrante(arreglo[i]):
			pass
		else:
			arreglo2.append(arreglo[i])
	return arreglo2

def es_palabra_sobrante(item):
	if item in palabras_sobrantes:
		return True
	return False

def palabra_en_texto(palabra,texto):
	for t in texto:
		if palabra==t.encode('utf8'):
			return True
	return False

database="db.development.sqlite"
conn=create_connection(database)
obtener_sesiones(conn)

palabras=[]
palabras+=quitar_palabras_sobrantes(texto)
for i in range(0,len(pistas)):
	palabras+=quitar_palabras_sobrantes(pistas[i])

palabras+=palabras_fijas

palabras = list(set(palabras))

resultados={}
for fila in filas:
	sesion = str(fila[0])
	estudiante = str(fila[1])
	texto = quitar_palabras_sobrantes(fila[2])
	for palabra in palabras:
		if palabra_en_texto(palabra,texto):
			try:
				resultados[sesion]
			except:
				resultados[sesion]={}
			s_dict = resultados[sesion]
			try:
				s_dict[estudiante]
			except:
				s_dict[estudiante]={}
			e_dict = s_dict[estudiante]
			try:
				e_dict[palabra]=e_dict[palabra]+1
			except:
				e_dict[palabra]=1

file=open("resultados.csv","w")
file.write("Sesion,Estudiante,Palabra,Frecuencia\n")
for session,value in resultados.iteritems():
	for estudiante,v in value.iteritems():
		for palabra_freq in v.iteritems():
			p= palabra_freq[0]
			f= palabra_freq[1]
			file.write(session+","+estudiante+","+p+","+str(f)+"\n")


file.close()

