import json
from flask import Flask
import mysql.connector


with open('config.json', 'r') as file:
    config_data = json.load(file)

app = Flask(__name__)

@app.route("/empleadosLista")

def obtenerLista():

  mydb = mysql.connector.connect(
    host=config_data['mydb']['host'],
    user=config_data['mydb']['user'],
    database=config_data['mydb']['database']
)
  mycursor = mydb.cursor()

  listaEmpleados = "SELECT * FROM empleados"

  mycursor.execute(listaEmpleados)

  myresult = mycursor.fetchall()
  
  # convert into JSON:
  y = json.dumps(myresult)

  # the result is a JSON string:
  return y

@app.route("/empleadosNuevo")

def AñadirUser():

  mydb = mysql.connector.connect(
    host=config_data['mydb']['host'],
    user=config_data['mydb']['user'],
    database=config_data['mydb']['database']
)
  mycursor = mydb.cursor()

  nombre = input("Nombre: ")
  idEmpleado = input("Id: ")
  rol = input("Rol: ")

  sql = "INSERT INTO empleados (nombre, id_empleado, rol) VALUES (%s, %s, %s)"
  val = (nombre, idEmpleado, rol)
  mycursor.execute(sql, val)

  mydb.commit()
  return "¡Añadido correctamente!"

