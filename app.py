import functools
import os
from validate_email import validate_email
import yagmail as yagmail
from flask import Flask, render_template, request, jsonify, redirect, session, send_file, g, url_for, flash, \
    send_from_directory
import utils
from formulario import Contactenos
from articulos import articulos
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice

app = Flask(__name__)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.path.abspath("./static/img/carpeta")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

##sfasfa
@app.route('/')
def index():
    return render_template('login.html', nombre='')


@app.route('/procesar', methods=['POST'])
def procesar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
        yag.send(to=email, subject='Nueva cuenta',
                 contents='Para activar cuenta click aquí <a href="www.google.com"></a>')
        return render_template('menubo.html')


@app.route('/enivarcontraseña', methods=['POST'])
def enivarcontraseña():

        if request.method == 'POST':
            email = request.form['correo']
            db = get_db()
            user = db.execute('SELECT * FROM usuario WHERE correo = ?',
                          (email, )).fetchall()

            password = user[0][3]
            yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
            yag.send(to=email, subject='Recuperar Contraseña',
                 contents='Para su registro esta son sus credenciales <br> Correo:' + email + '<br> Contraseña:' + password)
            return redirect(url_for('login'))


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/menu')
def menu():
    return render_template('menubo.html')


@app.route("/crear")
def crear():
    return render_template('Crear.html')


@app.route('/crearProducto')
def crearProducto():
    return render_template('crearproducto.html')


@app.route('/recuperar')
def recuperar():
    return render_template('Recuperar.html')


@app.route('/GuardaryEliminar')
def GuardaryEliminar():
    return render_template('GuardaryEliminar.html')


@app.route('/GuardaryEliminarUsuario')
def GuardaryEliminarUsuario():
    return render_template('GuardaryEliminarUsuario.html')


@app.route('/sesionlunes')
def lunes():
    form = Contactenos()
    return render_template('contacto.html', titulo='Contactenos', form=form)


@app.route('/sesion15')
def sesion15():
    return jsonify({"aticulogit a": articulos})


app.route('/articulos/<string:nombrearticulo')


def getarticulo(nombrearticulo):
    buscar = [articulo for articulo in articulos if articulo['nombre'] == nombrearticulo]
    if (len(buscar) > 8):
        return
    return jsonify({'message': 'articulo no encontrado '})


@app.route('/register', methods=('POST', 'GET'))
def register():
    try:
        if request.method == 'POST':
            usuario = request.form['usuario']
            email = request.form['email']
            longitud = 9
            valores = '123456789abcdefghijklmnopqrstuABCEDEFGHIJKLMNUOPARAS+-*'
            password = ''
            password = password.join([choice(valores) for i in range(longitud)])
            haspass = generate_password_hash(password)
            db = get_db()
            error = None

            db.execute(
                'INSERT INTO usuario (usuario, correo, contraseña, esadmin ) VALUES (?,?,?,?)',
                (usuario, email, haspass, False)
            )
            db.commit()
            yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
            yag.send(to=email, subject='Nueva cuenta',
                     contents='Para su registro esta son sus credenciales <br> Usuario:' + usuario + '<br> Contraseña:' + password)
            return redirect(url_for('recorrer'))

    except:
        error = 'Usuario o contraseña invalido'
        flash(error)
        return redirect(url_for('crear'))


@app.route('/registerProducto', methods=('POST', 'GET'))
def registerProducto():
    try:
        if request.method == 'POST':
            referencia = request.form['nombreProducto']
            cantidad = request.form['cantidad']
            error = None
            a = request.files['name']
            nombre = a.filename
            disponible = "Editar"
            a.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre))

            db = get_db()
            db.execute(
                'INSERT INTO producto (referencia, cantidad, imagen , disponible ) VALUES (?,?,?,?)',
                (referencia, cantidad, nombre, disponible)
            )
            db.commit()

            return redirect(url_for('recorrer'))
    except:
        message = 'Debe llenar todos los campos e insertar una imagen'
        flash(message)
        return redirect(url_for('crearProducto'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view


@app.route('/verificar', methods=('POST', 'GET'))
def verificar():
    try:
        if request.method == 'POST':
            usuarios = request.form['user']
            password = request.form['password']
            db = get_db()
            user = db.execute('SELECT * FROM usuario WHERE usuario = ?',
                              (usuarios,)).fetchall()
            var = user[0][4]
            var1 = user[0][3]

            if var == 1 and var1 == password:
                return redirect(url_for('recorrer'))

            if check_password_hash(user[0][3], password):
                session.clear()
                session['user_id'] = user[0]
                if var == 0:
                    return redirect(url_for('recorre'))

            else:
                message = 'Usuario o contraseña invalido'
                flash(message)
                return redirect(url_for('login'))

    except:
        message = 'Usuario o contraseña invalido'
        flash(message)
        return redirect(url_for('login'))


@app.route('/recorre')
def recorre():
    db = get_db()
    userto = db.execute(
        'SELECT * FROM producto'
    ).fetchall()
    return render_template('menuUsuario.html', userto=userto)


@app.route('/recorrer')
def recorrer():
    db = get_db()
    userto = db.execute(
        'SELECT * FROM producto'
    ).fetchall()
    return render_template('menubo.html', userto=userto)


@app.route('/abrirProducto', methods=('POST', 'GET'))
def abrirProducto():
    db = get_db()
    id = request.form['error']
    userto = db.execute('SELECT * FROM producto WHERE id = ?',
                        (id,)).fetchall()
    referencia = userto[0][1]
    cantidad = userto[0][2]
    imagen = userto[0][3]

    return render_template('GuardaryEliminarUsuario.html', referencia=referencia, cantidad=cantidad, imagen=imagen,id=id)


@app.route('/abrirProductoAdmin', methods=('POST', 'GET'))
def abrirProductoAdmin():
    db = get_db()
    id = request.form['error']
    userto = db.execute('SELECT * FROM producto WHERE id = ?', (id,)).fetchall()
    referencia = userto[0][1]
    cantidad = userto[0][2]
    imagen = userto[0][3]

    return render_template('GuardaryEliminar.html', referencia=referencia, cantidad=cantidad, imagen=imagen, id=id)


@app.route('/actualizarDatos', methods=('POST', 'GET'))
def actualizarDatos():
    try:
        if request.method == 'POST':
            referencias = request.form['nombreProducto']
            cantidades = request.form['Cantidad']
            id = request.form['id']
            error = None
            db = get_db()
            db.execute(
                    'UPDATE producto SET cantidad = ? WHERE id = ?', (cantidades, id)
                )
            db.commit()

            return redirect(url_for('recorre'))
    except:
        return redirect(url_for('recorre'))


@app.route('/actualizarDatosAdmin', methods=('POST', 'GET'))
def actualizarDatosAdmin():
    try:
        if request.method == 'POST':
            referencias = request.form['nombreProducto']
            cantidades = request.form['Cantidad']
            id = request.form['id']
            error = None
            db = get_db()
            db.execute(
                'UPDATE producto SET cantidad = ?, referencia = ? WHERE id = ?', (cantidades,referencias, id)
            )
            db.commit()
            return redirect(url_for('recorrer'))
    except:
        return redirect(url_for('recorrer'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/eliminar', methods=('POST', 'GET'))
def eliminar():
    try:
        if request.method == 'POST':
            ide = request.form['id']
            db = get_db()
            db.execute(
                'UPDATE producto SET disponible = "No disponible" WHERE id = ?', (ide, )
            )
            db.commit()
            return redirect(url_for('recorrer'))
    except:
        return redirect(url_for('recorrer'))


if __name__ == '__main__':
    app.run()
