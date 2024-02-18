import json
from flask import Flask, jsonify, request, render_template
import mysql.connector


with open('config.json', 'r') as file:
    config_data = json.load(file)

app = Flask(__name__)


#Vista índice, para ir a empleados, productos, o detalles de producto.
@app.route("/")
def vistaPrincipal():
    return render_template("index.html")


#Vista empleados, para acceder a los distintos endpoints
@app.route("/empleados")
def vistaEmpleados():
    return render_template("empleados.html")


#Endpoint que devuelve una lista de empleados, filtrado porque el rol sea de empleado
@app.route("/empleadosLista/<rol>", methods = ["GET"])
def obtenerLista(rol):
    try:
        mydb = mysql.connector.connect(
            host=config_data['mydb']['host'],
            user=config_data['mydb']['user'],
            database=config_data['mydb']['database']
        )

        mycursor = mydb.cursor()


        sql = ("SELECT * FROM empleados WHERE rol = %s")
        val = (rol,)
        # Consulta select con el filtrado de empleado
        mycursor.execute(sql,val)

        # Recuperar todas las filas del resultado
        myresult = mycursor.fetchall()
        
        #Nombre de las columnas, a través del .description
        columnasTabla = [i[0] for i in mycursor.description]

            # Crear una lista de diccionarios, cada uno representando a un empleado
        listaEmpleados = [
        {columnasTabla[i]: columna[i] for i in range(len(columnasTabla))}
        for columna in myresult
        ]

        # Convertimos esa lista en un json y lo mostramos
        return json.dumps(listaEmpleados)
    except Exception as e:
        return str(e), 400
        


#Endpoint que añade un nuevo usuario
@app.route("/empleadoNuevo", methods=["POST"])

def AñadirEmpleado():

    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Extraer los valores del diccionario JSON
        nombre = data["nombre"]
        id_empleado = data["id_empleado"]
        rol = data["rol"]

        
        mydb = mysql.connector.connect(
            host=config_data['mydb']['host'],
            user=config_data['mydb']['user'],
            database=config_data['mydb']['database']
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO empleados (nombre, id_empleado, rol) VALUES (%s, %s, %s)"
        val = (nombre, id_empleado, rol)
        mycursor.execute(sql, val)

        mydb.commit()

        return jsonify({"mensaje": "Correcto!"}), 200
    except Exception as e:
        return jsonify({"Error"}),400  
    

#Endpoint modificar rol del empleado
@app.route("/modificarEmpleado/<id>", methods=["POST"])
def modificarEmpleado(id):
    try:
        data=request.get_json()

        nuevoNombre=data["nuevoNombre"]
        nuevoRol = data["nuevoRol"]

        mydb = mysql.connector.connect(
                host=config_data['mydb']['host'],
                user=config_data['mydb']['user'],
                database=config_data['mydb']['database']
            )

        mycursor = mydb.cursor()

        sql = ("UPDATE empleados SET rol = %s, nombre = %s WHERE id_empleado=%s")
        val=(nuevoRol,nuevoNombre,id,)
        mycursor.execute(sql,val)

        mydb.commit()

        return {"mensaje": "Ok"}, 200
    except Exception as e:
        return {"Error": str(e)}, 400

@app.route("/eliminarEmpleado/<id>", methods=["DELETE"])

def eliminarEmpleado(id):
    try:
        mydb = mysql.connector.connect(
            host=config_data['mydb']['host'],
            user=config_data['mydb']['user'],
            database=config_data['mydb']['database']
        )

        mycursor = mydb.cursor()

        sql = "DELETE FROM empleados WHERE id_empleado = %s"
        val = (id,)
        mycursor.execute(sql, val)

        mydb.commit()

        return {"mensaje": "Ok"}, 200
    except Exception as e:
        return {"Error": str(e)}, 400
    
@app.route("/empleado/<id>", methods = ["GET"])
def obtenerEmpleado(id):
    try:
        mydb = mysql.connector.connect(
            host=config_data['mydb']['host'],
            user=config_data['mydb']['user'],
            database=config_data['mydb']['database']
        )

        mycursor = mydb.cursor()

        sql = "SELECT * FROM empleados WHERE id_empleado = %s"
        val = (id,)
        mycursor.execute(sql, val)

        myresult = mycursor.fetchone()

        columnasTabla = [i[0] for i in mycursor.description]

        empleado = {columnasTabla[i]: myresult[i] for i in range(len(columnasTabla))}
        

        return json.dumps(empleado)
    except Exception as e:
        return {"Error": str(e)}, 400



#   EndPoints Tabla Productos - Jorge Reina Romero
    
@app.route("/listaProductos/<marca>", methods = ["GET"])
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


@app.route("/añadirProducto", methods=["POST"])
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
def modificarProducto(id_producto):
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
def eliminarProducto(id_producto):
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
def obtenerProducto(id_producto):
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
  
#   EndPoints Tabla detalleproducto - Amanda Navas Rodriguez
  
#Ver todos los detalles de un producto segun su id
@app.route("/detalleProducto/<id_producto>", methods=["GET"])
def detalleProducto(id_producto):
  try:
    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database =config_data['mydb']['database']
    )
      
    mycursor = mydb.cursor()

    sql = "SELECT * FROM detalleproducto WHERE id_producto = %s"
    val = (id_producto,)

    mycursor.execute(sql, val)

    myresult = mycursor.fetchone()

    columnasTabla = [i[0] for i in mycursor.description]
    detalleproducto = {columnasTabla[i]: myresult[i] for i in range(len(columnasTabla))}
    
    return json.dumps(detalleproducto)
  except Exception as e:
    return{"Error": str(e)}, 400

#Crear detalles de un producto segun su id
@app.route("/añadirDetalleProducto", methods=["POST"])
def añadir_detalleProducto():
  try:
    data = request.get_json()

    precio = data["precio"]
    fecha = data["fecha"]
    url = data["url"]
    modelo = data["modelo"]
    id_producto = data["id_producto"]

    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO detalleproducto (precio, fecha, url, modelo, id_producto) VALUES (%s, %s, %s, %s, %s)"
    val = (precio, fecha, url, modelo, id_producto)
    mycursor.execute(sql, val)

    mydb.commit()
    
    return jsonify({"mensaje" : "OK"}), 200
  except Exception as e:
    return {"Error": str(e)}, 400


#Modificar detalles de un producto segun su id
@app.route("/modificarDetalleProducto/<id_producto>", methods=["POST"])
def modificar_detalleProducto(id_producto):
  try:
    data=request.get_json()

    precio = data["precio"]
    fecha = data["fecha"]
    url = data["url"]
    modelo = data["modelo"]


    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    sql = "UPDATE detalleproducto SET precio = %s, fecha = %s, url = %s, modelo = %s WHERE id_producto = %s"
    val = (precio, fecha, url, modelo, id_producto)
    mycursor.execute(sql, val)

    mydb.commit()

    return {"mensaje": "Ok"}, 200
  except Exception as e:
      return {"Error": str(e)}, 400

#ELiminar detalles de un producto segun su id
@app.route("/eliminarDetalleProducto/<id_producto>", methods=["DELETE"])
def eliminar_detalleProducto(id_producto):
  try:
    mydb = mysql.connector.connect(
      host=config_data['mydb']['host'],
      user=config_data['mydb']['user'],
      database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    sql = "DELETE FROM detalleproducto WHERE id_producto = %s"
    val = (id_producto,)
    mycursor.execute(sql, val)

    mydb.commit()

    return {"mensaje": "Ok"}, 200
  except Exception as e:
    return {"Error": str(e)}, 400

app.config['STATIC_FOLDER'] = 'static'


