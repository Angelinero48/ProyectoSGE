import json
from flask import Flask, request, render_template
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
@app.route("/empleadosLista")
def obtenerLista():
    mydb = mysql.connector.connect(
        host=config_data['mydb']['host'],
        user=config_data['mydb']['user'],
        database=config_data['mydb']['database']
    )

    mycursor = mydb.cursor()

    # Consulta select con el filtrado de empleado
    mycursor.execute("SELECT * FROM empleados WHERE rol='empleado'")

    # Recuperar todas las filas del resultado
    myresult = mycursor.fetchall()

    # Verificar si se obtuvieron resultados
    if myresult:
        #Nombre de las columnas, a través del .description
        column_names = [i[0] for i in mycursor.description]

        # Crear una lista de diccionarios, cada uno representando a un empleado
        employees_dict_list = [
            {column_names[i]: row[i] for i in range(len(column_names))}
            for row in myresult
        ]

        # Convertimos esa lista en un json y lo mostramos
        return json.dumps(employees_dict_list)
    else:
        return "No se encontraron resultados."


#Endpoint que añade un nuevo usuario
@app.route("/empleadosNuevo", methods=["POST"])

def AñadirEmpleado():

    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.get_json()

        # Extraer los valores del diccionario JSON
        nombre = data["nombre"]
        id_empleado = data["id_empleado"]
        rol = data["rol"]

        # Conectar a la base de datos y realizar la inserción
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

        return "¡Añadido correctamente!"
    except Exception as e:
        return str(e), 400  # Devolver un mensaje de error y código de estado 400 en caso de problemas
    

#Endpoint modificar rol del empleado
@app.route("/modificarEmpleado", methods=["PUT"])
def modificarEmpleado():
    
    data=request.get_json()

    id_empleado = data["id_empleado"]
    nuevoRol = data["nuevoRol"]

    mydb = mysql.connector.connect(
            host=config_data['mydb']['host'],
            user=config_data['mydb']['user'],
            database=config_data['mydb']['database']
        )

    mycursor = mydb.cursor()

    sql = ("UPDATE empleados SET rol = %s WHERE id_empleado=%s")
    val=(nuevoRol,id_empleado)
    mycursor.execute(sql,val)

    mydb.commit()

    return "¡Empleado modificado correctamente!"

    app.config['STATIC_FOLDER'] = 'static'


