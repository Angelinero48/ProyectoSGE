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
        column_names = [i[0] for i in mycursor.description]

            # Crear una lista de diccionarios, cada uno representando a un empleado
        employees_dict_list = [
        {column_names[i]: row[i] for i in range(len(column_names))}
        for row in myresult
        ]

        # Convertimos esa lista en un json y lo mostramos
        return json.dumps(employees_dict_list)
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



    app.config['STATIC_FOLDER'] = 'static'


