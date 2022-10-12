from pony.orm import *

db = Database()

db.bind(provider="sqlite", filename="main.db", create_db=True)


class TestMessage(db.Entity):
    msgid = PrimaryKey(int, auto=True)
    text = Required(str, 255)


class Usuario(db.Entity):
    user_id = PrimaryKey(int, auto=True)
    nombre_usuario = Required(str, 255, unique=True)
    email = Required(str, 255, unique=True)
    contraseña = Required(str, 255)
    avatar = Optional(str, 255)
    verificado = Required(bool)
    robot = Set('Robot', reverse='usuario')
    partida = Set('Partida', reverse='creador')


class Robot(db.Entity):
    robot_id = PrimaryKey(int, auto=True)
    nombre = Required(str, 255)
    implementacion = Required(str, 255)
    avatar = Optional(str, 255)
    partidas_ganadas = Required(int)
    partidas_jugadas = Required(int)
    defectuoso = Required(bool)
    participa = Set('Partida', reverse='participante')
    usuario = Required(Usuario, reverse='robot')
    gano = Set('Partida', reverse='ganador')


class Partida(db.Entity):
    partida_id = PrimaryKey(int, auto=True)
    nombre = Required(str, 255)
    contraseña = Optional(str, 255)
    status = Required(str, 32)
    cant_jugadores = Required(int)
    cant_juegos = Required(int)
    cant_rondas = Required(int)
    participante = Set(Robot, reverse='participa')
    creador = Required(Usuario, reverse='partida')
    ganador = Optional(Robot, reverse='gano')


db.generate_mapping(create_tables=True)


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
    upper=any(c.isupper() for c in pas)
    lower=any(c.islower() for c in pas)
    digit=any(c.isdigit() for c in pas)
    return (upper) and (lower) and (digit)
   

#  Crea al usuario con el nombre, el password y el email introducido.
def crear_usuario(name: str, password: str, myemail: str):
    Usuario(
        nombre_usuario=name,
        contraseña=password,
        email=myemail,
        verificado=True,
        avatar="Default Avatar"
    )
    