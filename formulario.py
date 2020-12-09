from wtforms import Form, SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import  DataRequired

class Contactenos(Form):
    nombre = StringField('Nombre', validators=[DataRequired(message='No dejar vacío, completar')])
    correo = EmailField('Correo',validators= [DataRequired(message="No dejar vacío, completar")])
    mensaje = StringField('Mensaje', validators=[DataRequired(message='No dejar vacío, completar')])
    password = PasswordField('Password', validators=[DataRequired()])
    enviar = SubmitField('Enviar Mensaje')