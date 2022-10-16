from pony.orm import *
from db import *


#  Verifica si el nombre de usuario existe
def user_exist(username: str):
    if Usuario.get(nombre_usuario=username) is not None:
        return True
    else:
        return False

#  Verifica si el email ya está registrado


def email_exist(email: str):
    if Usuario.get(email=email) is not None:
        return True
    else:
        return False


#  Verifica que el password tengo al menos una mayuscula,
#  al menos una minuscula y al menos un numero
def password_is_correct(pas: str):
    upper = any(c.isupper() for c in pas)
    lower = any(c.islower() for c in pas)
    digit = any(c.isdigit() for c in pas)
    return (upper) and (lower) and (digit)


# Se fija si los datos de logue ingresados son válidos


def correct_login(name: str, password: str):
    if Usuario.get(nombre_usuario=name, contraseña=password) is not None:
        return True
    else:
        return False

# Genera un diccionario con los datos ingresados


def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}
