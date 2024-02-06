from flask import Flask
import mysql.connector
import json

app = Flask(__name__)

#Ver todos los detalles de los productos
@app.route("/detalleProducto")
def select_detalleproducto():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database ="homies"
  )
    
  mycursor = mydb.cursor()

  mycursor.execute("SELECT * FROM detalleproducto")

  myresult = mycursor.fetchall()

  #convert into JSON:
  y = json.dumps(myresult)

  # the result is a JSON string:
  return y

#Crear detalles de un producto /<id_producto>, methods=['POST']
@app.route("/crearDetalleProducto")
def AñadirDetalleProducto():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="homies"
  )

  mycursor = mydb.cursor()

  sql = "INSERT INTO detalleproducto (precio, fecha, url, modelo, id_producto) VALUES (%s, %s, %s, %s, %s)"
  val = ("130", "06/02/24", "blablabla", "air force", "1")
  mycursor.execute(sql, val)

  mydb.commit()
  print("Detalle de producto añadido")


#editar el campo modelo de la tabla detalle producto
@app.route("/editarDetalleProducto")
def editarDetalleProducto():
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="homies"
  )

  mycursor = mydb.cursor()

  sql = "UPDATE detalleproducto SET modelo = 'air max' WHERE modelo = 'airforce'"
  mycursor.execute(sql)

  mydb.commit()
  print("Detalle de producto actualizado")



"""mycursor = mydb.cursor()

sql = "INSERT INTO empleados (nombre, id_empleado, rol) VALUES (%s, %s, %s)"
val = ("Amanda", "3", "Admin")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")"""