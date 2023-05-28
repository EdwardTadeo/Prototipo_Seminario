from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from random import randint
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'riesgo_crediticio'

mysql = MySQL(app)
print(app.config['MYSQL_HOST'])
print(app.config['MYSQL_USER'])
print(app.config['MYSQL_PASSWORD'])
print(app.config['MYSQL_DB'])

app.secret_key = '849342894378923487942378942387923478934278934278923418794317890'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND contraseña = %s', (username, password))
        data = cursor.fetchone()
        print(data)
        cursor.close()

        if data:
            session['email'] = username
            session['nombre'] = data[1]
            session['apellido'] = data[2]
            return redirect(url_for('main_menu'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'error')
            return render_template('index.html')

    return render_template('index.html')

@app.route('/main_menu')
def main_menu():
    if 'email' not in session: # Verifica si el usuario está autenticado
        return redirect(url_for('index'))
    else:
        # Obtén el nombre y apellido del usuario a través del correo electrónico
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT nombre, apellido FROM usuarios WHERE email = %s', (session['email'],))
        user_data = cursor.fetchone()
        print(user_data)
        cursor.close()
        if user_data:
            # Pasa el nombre y apellido del usuario a la plantilla 'menu.html' utilizando un argumento de contexto
            return render_template('main_menu.html')
    return render_template('main_menu.html')

@app.route('/gestion_usuarios')
def gestion_usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_usuario, nombre, apellido, email FROM usuarios')
    users = cursor.fetchall()
    print(users)
    cursor.close()
    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'nombre': user[1], 'apellido': user[2], 'email': user[3]}
        user_list.append(user_dict)
    return render_template('gestion_usuarios.html', users=user_list)

@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        user_id = request.json['id']
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        email = request.json['email']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE `riesgo_crediticio`.`usuarios` SET `nombre` = %s, `apellido` = %s, `email` = %s WHERE (`id_usuario` = %s)',(nombre, apellido, email, user_id))

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'El usuario se actualizó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        user_id = request.json['id']
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM `riesgo_crediticio`.`usuarios` WHERE (`id_usuario` = %s)', (user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'El usuario se elimino correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        email = request.json['email']
        contraseña = nombre+'123'
        rol = 1
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO `riesgo_crediticio`.`usuarios` (`nombre`, `apellido`, `email`, `contraseña`, `id_rol`) VALUES (%s, %s, %s,%s,%s)', (nombre, apellido, email, contraseña, rol))

        mysql.connection.commit()
        cursor.close()

        # Obtener el ID del usuario recién insertado
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT LAST_INSERT_ID()')
        user_id = cursor.fetchone()[0]
        cursor.close()

        return jsonify({'id': user_id, 'message': 'El usuario se agregó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gestion_categorias')
def gestion_categorias():
    return render_template('gestion_categorias.html')

@app.route('/evaluacion_dataset')
def evaluacion_dataset():
    return render_template('evaluacion_dataset.html')

@app.route('/ingresar_datos_solicitantes')
def ingresar_datos_solicitante():
    return render_template('ingresar_datos_solicitantes.html')



@app.route('/consultar_cliente', methods=['POST'])
def add_cliente():
    
    dni = request.json['dni']
    print(dni)
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT nombre, apellido, email, telefono, direccion '
                       'FROM clientes WHERE dni = %s', (dni,))
    cliente = cursor.fetchone()
    print(cliente)
    cursor.close()
    if cliente:
        return jsonify({'cliente': cliente})
    else:
        mensaje = "Este cliente no ha solicitado un préstamo previamente."
        return jsonify({'mensaje': mensaje})

@app.route('/registrar_prestamo', methods=['POST'])
def registrar_prestamo():
    try:
        dni = 1
        ingresos_mensuales = request.json['ingresos-mensuales']
        egresos_mensuales = request.json['egresos-mensuales']
        monto_solicitado = request.json['monto-solicitado']
        tiempo_prestamo = request.json['tiempo-prestamo']
        tipo_empleo = request.json['tipo-empleo']
        tiempo_empleo = request.json['tiempo-empleo']
        nivel_educativo = request.json['nivel-educativo']
        estado_civil = request.json['estado-civil']
        num_dependientes = request.json['dependientes']
        edad = request.json['edad']
        historial_vivienda = request.json['historial-vivienda']
        proposito_prestamo = request.json['proposito-prestamo']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO datos_prestamo (id_cliente, ingresos_mensuales, egresos_mensuales, monto_solicitado, tiempo_prestamo, tipo_empleo, tiempo_empleo, nivel_educativo, estado_civil, num_dependientes, edad, historial_vivienda, proposito_prestamo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (dni, ingresos_mensuales, egresos_mensuales, monto_solicitado, tiempo_prestamo, tipo_empleo, tiempo_empleo, nivel_educativo, estado_civil, num_dependientes, edad, historial_vivienda, proposito_prestamo))
        mysql.connection.commit()
        cursor.close()
        
        return render_template('ingresar_datos_solicitantes.html')
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/gestion_solicitante')
def gestion_solicitante():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id_cliente, nombre, apellido, dni, email, telefono, direccion FROM clientes')
    users = cursor.fetchall()
    print(users)
    cursor.close()
    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'nombre': user[1], 'apellido': user[2], 'dni': user[3], 'email': user[4], 'telefono': user[5], 'direccion': user[6] }
        user_list.append(user_dict)
    return render_template('gestion_solicitante.html', users=user_list)

@app.route('/update_cliente', methods=['POST'])
def update_cliente():
    try:
        user_id = request.json['id']
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        dni = request.json['dni']
        email = request.json['email']
        telefono = request.json['telefono']
        direccion = request.json['direccion']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE `riesgo_crediticio`.`clientes` SET `nombre` = %s, `apellido` = %s, `dni` = %s, `email` = %s, `telefono` = %s, `direccion` = %s WHERE (`id_cliente` = %s)',(nombre, apellido, dni, email, telefono, direccion, user_id))

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'El usuario se actualizó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/delete_cliente', methods=['POST'])
def delete_cliente():
    try:
        user_id = request.json['id']
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM `riesgo_crediticio`.`clientes` WHERE (`id_cliente` = %s)', (user_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'El usuario se elimino correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_cliente', methods=['POST'])
def adds_cliente():
    try:
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        dni = request.json['dni']
        email = request.json['email']
        telefono = request.json['telefono']
        direccion = request.json['direccion']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO `riesgo_crediticio`.`clientes` (`nombre`, `apellido`, `dni`, `email`, `telefono`, `direccion`) VALUES (%s, %s, %s,%s,%s, %s)', (nombre, apellido, dni, email, telefono, direccion))

        mysql.connection.commit()
        cursor.close()

        # Obtener el ID del usuario recién insertado
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT LAST_INSERT_ID()')
        user_id = cursor.fetchone()[0]
        cursor.close()

        return jsonify({'id': user_id, 'message': 'El usuario se agregó correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/seguimiento_solicitante', methods=['GET', 'POST'])
def seguimiento_solicitante():
    if request.method == 'POST':
        dni = request.form['dni']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT dp.*, s.* FROM datos_prestamo dp INNER JOIN clientes c ON c.id_cliente = dp.id_cliente LEFT JOIN seguimiento s ON s.id_prestamo = dp.id_prestamo WHERE c.dni = %s', (dni,))
        data_prestamos = cursor.fetchall()
        cursor.close()

        if data_prestamos:
            return render_template('seguimiento_solicitante.html', data_prestamos=data_prestamos)
        else:
            mensaje = "Este cliente no ha solicitado un préstamo previamente."
            return render_template('seguimiento_solicitante.html', mensaje=mensaje)
    else:
        return render_template('seguimiento_solicitante.html')
    

@app.route('/evaluar_solicitante', methods = ['GET','POST'])
def evaluar_solicitante():
    if request.method == 'POST':
        dni = request.form['dni']
        cursor = mysql.connection.cursor()
        estado = 'En proceso de evaluación'
        cursor.execute ('SELECT CONCAT(c.nombre, " ", c.apellido) AS nombre_completo, dp.*, s.* FROM datos_prestamo dp INNER JOIN clientes c ON c.id_cliente = dp.id_cliente LEFT JOIN seguimiento s ON s.id_prestamo = dp.id_prestamo WHERE c.dni = %s AND s.estado = %s', (dni, estado))
        data_result = cursor.fetchall()
        print(data_result)
        cursor.close()
        if data_result:
            return render_template('evaluar_solicitante.html', data_result=data_result, randint=randint)
        else:
            mensaje = "Este cliente no tiene un proceso de evaluacion activo"
            return render_template('evaluar_solicitante.html', mensaje=mensaje)
    else:
        return render_template('evaluar_solicitante.html')



if __name__ == '__main__':
    app.run()
