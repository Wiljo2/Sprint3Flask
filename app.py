import os
import yagmail as yagmail
from flask import Flask, render_template, request, jsonify
from utils import isEmailValid, isUsernameValid, isPasswordValid
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
        return render_template('Crear.html', nombre='')

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
        if request.method == 'POST':
            usuario = request.form['usuario']
            email = request.form['email']
            password = request.form['password']
            error = None
            db = get_db()
            db.execute(
                'INSERT INTO usuario (usuario, correo, contraseña) VALUES (?,?,?)',
                (usuario, email, password)
            )
            db.commit()
            yag = yagmail.SMTP('proyectosprint3@gmail.com', 'qwaszx013654')
            yag.send(to=email, subject='Nueva cuenta', contents='Activar cuenta<a href="www.google.com">clic aqui</a>')
            return render_template('Crear.html')

if __name__ == '__main__':
    app.run()

