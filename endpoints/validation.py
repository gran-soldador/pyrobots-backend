from pony.orm import *
from db import *
import yagmail
from os import getenv

from endpoints.functions_jwt import gen_verification_token


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
    app_password = getenv("GMAIL_APP_PW")  # a token for gmail
    token = gen_verification_token({'email': mail})
    link = f"http://localhost:3000/verify/{token}"  # TODO: Get URL from env
    subject = 'Verifica tu cuenta de PYRobot'
    content = f"""
<a href="{link}">Clickeá aca para verificar tu cuenta en PYRobots</a>
En caso de que no funcione, copia y pega el siguiente link en tu navegador:
{link}
"""
    with yagmail.SMTP(user, app_password) as yag:
        yag.send(mail, subject, content)


# Envía correo electronico con link para recuperar contraseña
def send_email_recover(mail: str):
    user = 'emaildepruebagransoldador@gmail.com'
    app_password = getenv("GMAIL_APP_PW")  # a token for gmail
    token = gen_verification_token({'email': mail})
    link = f"http://localhost:3000/verify/{token}"  # TODO: Get URL from env
    subject = 'Recuperá la contraseña de tu cuenta en PYRobots.'
    content = f"""
<a href="{link}">Clickeá aca para recuperar la contraseña de tu cuenta</a>
En caso de que no funcione, copia y pega el siguiente link en tu navegador:
{link}
"""
    with yagmail.SMTP(user, app_password) as yag:
        yag.send(mail, subject, content)
