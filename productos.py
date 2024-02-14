import json
from flask import Flask, jsonify, request
import mysql.connector

with open('config.json', 'r') as file:
  config_data = json.load(file)

app = Flask(__name__)

@app.route("/ListaProductos/<marca>", methods = ["GET"])
def lista_producto(marca):
  try:
    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    sql = ("SELECT * FROM productos WHERE marca = %s")
    val = (marca,)

    mycursor.execute(sql, val)

    #Recuperar todas las filas del resultado
    myresult = mycursor.fetchall()

    
      
    column_names = [i[0] for i in mycursor.description]

    empleoyees_dict_list = [
      {column_names[i]: row[i] for i in range(len(column_names))}
      for row in myresult
    ]

    return json.dumps(empleoyees_dict_list)
  except Exception as e:
    return str(e), 400
  

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


@app.route("/modificarProducto/<id_producto>", methods=["POST"])
def modificarEmpleado(id_producto):
  try:
      data=request.get_json()

      nombre = data["nombre"]
      marca = data["marca"]
      modelo = data["modelo"]
      id_empleado = data["id_empleado"]

      mydb = mysql.connector.connect(
        host=config_data['mydb']['host'],
        user=config_data['mydb']['user'],
        database=config_data['mydb']['database']
      )

      mycursor = mydb.cursor()

      sql = ("UPDATE productos SET nombre = %s, marca = %s, modelo = %s, id_empleado = %s WHERE id_producto=%s")
      val=(nombre,marca, modelo, id_empleado,id_producto,)
      mycursor.execute(sql,val)

      mydb.commit()

      return {"mensaje": "Ok"}, 200
  except Exception as e:
      return {"Error": str(e)}, 400
  
@app.route("/eliminarProducto/<id_producto>", methods=["DELETE"])
def eliminarEmpleado(id_producto):
  try:
    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    sql = "DELETE FROM productos WHERE id_producto = %s"
    val = (id_producto,)
    mycursor.execute(sql, val)

    mydb.commit()

    return {"mensaje": "Ok"}, 200
  except Exception as e:
    return {"Error": str(e)}, 400


@app.route("/producto/<id_producto>", methods = ["GET"])
def obtenerEmpleado(id_producto):
  try:
    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    sql = "SELECT * FROM productos WHERE id_producto = %s"
    val = (id_producto,)
    mycursor.execute(sql, val)

    myresult = mycursor.fetchone()

    columnasTabla = [i[0] for i in mycursor.description]

    empleado = {columnasTabla[i]: myresult[i] for i in range(len(columnasTabla))}
    

    return json.dumps(empleado)
  except Exception as e:
    return {"Error": str(e)}, 400