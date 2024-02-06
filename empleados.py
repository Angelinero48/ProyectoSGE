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

    # Ejecutar una consulta SELECT
    mycursor.execute("SELECT * FROM empleados")

    # Recuperar todas las filas del resultado
    myresult = mycursor.fetchall()

    # Verificar si se obtuvieron resultados
    if myresult:
        # Obtener los nombres de las columnas
        column_names = [i[0] for i in mycursor.description]

        # Crear una lista de diccionarios, cada uno representando a un empleado
        employees_dict_list = [
            {column_names[i]: row[i] for i in range(len(column_names))}
            for row in myresult
        ]

        # Convertir la lista de diccionarios en JSON y devolverla
        return json.dumps(employees_dict_list)
    else:
        return "No se encontraron resultados."

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

