import json
from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route("/ListaProductos")

def hello_world():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="homies"
  )

  mycursor = mydb.cursor()

  productos = "SELECT * FROM productos"

  mycursor.execute(productos, { 'name': 0})
  #mycursor.execute(marca_productos)
  #mycursor.execute(modelo_producto)
  #mycursor.execute(id_producto)

  bd = mycursor.execute(productos, { 'name': 0})
  bd2 = str(bd)

  #convert into JSON:
  products_json = json.dumps(bd)

  # the result is a JSON string:
  return products_json


