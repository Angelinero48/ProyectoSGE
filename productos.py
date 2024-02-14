import json
from flask import Flask, jsonify, request
import mysql.connector

with open('config.json', 'r') as file:
  config_data = json.load(file)

app = Flask(__name__)

@app.route("/ListaProductos")
def lista_producto():
  mydb = mysql.connector.connect(
    host=config_data['mydb']['host'],
    user=config_data['mydb']['user'],
    database=config_data['mydb']['database']
  )

  mycursor = mydb.cursor()

  mycursor.execute("SELECT * FROM productos")

  #Recuperar todas las filas del resultado
  myresult = mycursor.fetchall()

  if myresult:
    
    column_names = [i[0] for i in mycursor.description]

    empleoyees_dict_list = [
      {column_names[i]: row[i] for i in range(len(column_names))}
      for row in myresult
    ]

    return json.dumps(empleoyees_dict_list)
  else:
    return "No se encontraron resultados"
  

@app.route("/AñadirProducto", methods=["POST"])
def añadir_producto():

  try:
    # Obtener los datos del cuerpo de la solicitud en fomarto Json
    data = request.get_json()

    # Extraer los valores de los diccionarios
    nombre = data["nombre"]
    marca = data["marca"]
    modelo = data["modelo"]
    id_prodcuto = data["id_producto"]
    id_empleado = data["id_empleado"]

    # Conectar a la base de datos y realizar la inserción
    mydb = mysql.connector.connect(
      host = config_data['mydb']['host'],
      user = config_data['mydb']['user'],
      database = config_data['mydb']['database']
    )

    mycursor = mydb.cursor()
    
    sql = "INSERT INTO productos (nombre, marca, modelo, id_producto, id_empleado) VALUES (%s, %s, %s, %s, %s)"
    val = (nombre, marca, modelo, id_prodcuto, id_empleado)
    mycursor.execute(sql,val)

    mydb.commit()

    return jsonify({"mensaje" : "OK"}), 200

  except Exception as e:
    return str(e), 400 # Ddevuelve un mensaje de erro con codigo 400



