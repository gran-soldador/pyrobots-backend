from pony.orm import *
from db import *


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


# Me dice si el usuario ya tiene un robot suyo con ese nombre
def user_robot_already_exist(username: str, robotName: str):
    myUser = Usuario.get(nombre_usuario=username)
    if Robot.get(nombre=robotName) is not None:
        myRobotUser = Robot.get(nombre=robotName).usuario.user_id
        if (myRobotUser == myUser.user_id):
            return True
    return False
