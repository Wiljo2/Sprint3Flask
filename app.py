import functools
import os
from validate_email import validate_email
import yagmail as yagmail
from flask import Flask, render_template, request, jsonify,redirect,session,send_file,g,url_for,flash
import utils
from formulario import Contactenos
from articulos import articulos
from db import get_db

app = Flask(__name__)
app.secret_key = os.urandom( 24 )


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
    return jsonify({"aticulos":articulos})

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
            password = request.form['password']
            db = get_db()
            error = None
            if not utils.isEmailValid():
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
                return render_template('Crear.html')

            if not utils.isPasswordValid(password):
                error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número y 8 caracteres'
                flash(error)
                return render_template('Crear.html')

            if not utils.isEmailValid(email):
                error = 'Correo invalido'
                flash(error)
                return render_template('Crear.html')

            if db.execute('SELECT id FROM usuario WHERE correo = ?', (email,)).fetchone() is not None:
                error = 'El correo ya existe'.format(email)
                flash(error)
                return render_template('Crear.html')

                db.execute(
                    'INSERT INTO usuario (usuario, correo, contraseña, esadmin ) VALUES (?,?,?,?)',
                    (usuario, email, password, False)
                )
                db.commit()
                yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
                yag.send(to=email, subject='Nueva cuenta',contents='Para su registro esta son sus credenciales <br> Correo:' + email + '<br> Contraseña:' + password)
                return render_template('menubo.html')

            else:
                return render_template('Crear.html')
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
            user = db.execute('SELECT * FROM usuario WHERE usuario = ? AND contraseña = ?',
                              (usuarios,password)).fetchall()
            session.clear()
            session['user_id'] = user[0]
            var = user[0][4]
            if var == 1:
                return render_template('menubo.html')
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


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()

