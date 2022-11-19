import yagmail
from os import getenv

from .tokens import gen_verification_token


# Envía correo electronico con link para verificar su cuenta
def send_verification_email(mail: str):
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
def send_recovery_email(mail: str):
    user = 'emaildepruebagransoldador@gmail.com'
    app_password = getenv("GMAIL_APP_PW")  # a token for gmail
    token = gen_verification_token({'email': mail})
    link = f"http://localhost:3000/recover/{token}"  # TODO: Get URL from env
    subject = 'Recuperá la contraseña de tu cuenta en PYRobots.'
    content = f"""
<a href="{link}">Clickeá aca para recuperar la contraseña de tu cuenta</a>
En caso de que no funcione, copia y pega el siguiente link en tu navegador:
{link}
"""
    with yagmail.SMTP(user, app_password) as yag:
        yag.send(mail, subject, content)
