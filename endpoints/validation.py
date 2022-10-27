from pony.orm import *
from db import *
import base64

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




#  Convierte por ahora la imagen del path a string y momentaneamete
#  escribe un archivo encode.bin para tener el string
#  mas compacto para poder probar 

def image_to_string():
    with open("userUploads/robotAvatars/defaultAvatarRobot.png", "rb") as file:
        img = file.read()
        data = base64.encodebytes(img)#.decode('utf-8')
    with open('userUploads/robotAvatars/encode.bin', "wb") as file:
        file.write(data)
    return data
    #return json.dumps(data)