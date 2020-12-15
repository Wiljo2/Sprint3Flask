import functools
import os
from validate_email import validate_email
import yagmail as yagmail
from flask import Flask, render_template, request, jsonify,redirect,session,send_file,g,url_for,flash,send_from_directory
import utils
from formulario import Contactenos
from articulos import articulos
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from random import choice


app = Flask(__name__)
app.secret_key = os.urandom( 24 )
UPLOAD_FOLDER = os.path.abspath("./resources/")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('login.html', nombre='')

@app.route('/procesar',methods=['POST'])
def procesar():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
        yag.send(to=email, subject='Nueva cuenta', contents='Activar cuentaz<a href="www.google.com">clic aqui</a>')
        return render_template('menubo.html')


@app.route('/enivarcontraseña',methods=['POST'])
def enivarcontraseña():
    if request.method == 'POST':
        email = request.form['correo']
        yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
        yag.send(to=email, subject='Recuperacion de Contraseña', contents='Ingrese en el siguiente link para el cambio de su contraseña.<a href="www.google.com">clic aqui</a>')
        return render_template('Login.html', nombre='')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/menu')
def menu():
    return render_template('menubo.html')

@app.route('/crear')
def crear():
    return render_template('crear.html')


@app.route('/crearProducto')
def crearProducto():
    return render_template('crearproducto.html')

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/GuardaryEliminar')
def GuardaryEliminar():
    return render_template('GuardaryEliminar.html')

@app.route('/GuardaryEliminarUsuario')
def GuardaryEliminarUsuario():
    return render_template('GuardaryEliminarUsuario.html')


@app.route('/sesionlunes')
def lunes():
    form = Contactenos()
    return render_template( 'contacto.html', titulo='Contactenos', form=form )

@app.route('/sesion15')
def sesion15():
    return jsonify({"aticulogit a":articulos})

app.route('/articulos/<string:nombrearticulo')
def getarticulo (nombrearticulo):
    buscar = [articulo for articulo in articulos if articulo['nombre']==nombrearticulo]
    if (len(buscar)>8):
        return
    return jsonify({'message':'articulo no encontrado '})


@app.route( '/register', methods=('POST', 'GET') )
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
            yag.send(to=email, subject='Nueva cuenta',contents='Para su registro esta son sus credenciales <br> Correo:' + email + '<br> Contraseña:' + password)
            return render_template('menubo.html')

    except:
        error = 'Usuario o contraseña invalido'
        flash(error)
        return redirect(url_for('crear'))

@app.route( '/registerProducto', methods=('POST', 'GET') )
def registerProducto():
        if request.method == 'POST':
            referencia = request.form['nombreProducto']
            cantidad = request.form['cantidad']
            imagen = request.form['imagen']
            error = None
            db = get_db()
            db.execute(
                'INSERT INTO producto (referencia, cantidad, imagen ) VALUES (?,?,?)',
                (referencia, cantidad, imagen)
            )
            db.commit()

            return render_template('menubo.html')


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
                              (usuarios, )).fetchall()
            var = user[0][4]
            if var == 1:
                return redirect(url_for('recorrer'))
            if check_password_hash(user[0][3], password):
                session.clear()
                session['user_id'] = user[0]
                if var == 0:
                    return redirect(url_for('recorre'))

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
    return render_template('menuUsuario.html', userto = userto)

@app.route('/recorrer')
def recorrer():
    db = get_db()
    userto = db.execute(
        'SELECT * FROM producto'
    ).fetchall()
    return render_template('menubo.html', userto = userto)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()


@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == "POST":
        a = request.files['name']
        nombre=a.filename
        a.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre))
        return redirect(url_for('get_file', filename=nombre))

@app.route('/uploads/<filename>')
def get_file(filename):
    print(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

