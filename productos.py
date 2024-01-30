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

  listaEmpleados = "SELECT * FROM productos"

  mycursor.execute(listaEmpleados)

  myresult = mycursor.fetchall()

  #convert into JSON:
  y = json.dumps(myresult)

  # the result is a JSON string:
  return y


