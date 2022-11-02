from pony.orm import *
from db import *
import yagmail
from endpoints.functions_jwt import write_token

#  Verifica si el nombre de usuario existe
def user_exist(username: str):
    return Usuario.get(nombre_usuario=username) is not None


#  Verifica si el email ya está registrado
def email_exist(email: str):
    return Usuario.get(email=email) is not None


#  Verifica que el password tengo al menos una mayuscula,
#  al menos una minuscula y al menos un numero
def password_is_correct(pas: str):
    upper = any(c.isupper() for c in pas)
    lower = any(c.islower() for c in pas)
    digit = any(c.isdigit() for c in pas)
    return (upper) and (lower) and (digit)


# Se fija si los datos de logue ingresados son válidos
def correct_login(name: str, password: str):
    return Usuario.get(nombre_usuario=name, contraseña=password) is not None


# Envía correo electronico con link para verificar su cuenta
def send_email(mail: str):
    user = 'emaildepruebagransoldador@gmail.com'
    app_password = 'blzgkxlqypwmqfdv' # a token for gmail
    to = mail
    token = write_token({'email': mail})
    token = token['accessToken']
    link = "http://localhost:3000/verify/"+ token
    subject = 'Verifica tu cuenta de PYRobot'
    content = [f'<a href="{link}">Clickeá aca para verificar tu cuenta en PYRobots</a>\n',
               "En caso de que no funcione, copia y pega el siguiente link en tu navegador:\n",
               link 
              ]

    with yagmail.SMTP(user, app_password) as yag:
        yag.send(to, subject, content)
