from pony.orm import *
import sys

db = Database()

if "pytest" in sys.modules:
    db.bind(provider="sqlite", filename=":sharedmemory:")   
else:
    db.bind(provider="sqlite", filename="main.db", create_db=True)


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
    implementacion = Required(str)
    avatar = Optional(str, 255)
    partidas_ganadas = Required(int)
    partidas_jugadas = Required(int)
    defectuoso = Required(bool)
    participa = Set('Partida', reverse='participante')
    usuario = Required(Usuario, reverse='robot')
    gano = Set('Partida', reverse='ganador')


class Partida(db.Entity):
    partida_id = PrimaryKey(int, auto=True)
    namepartida = Required(str, 32)
    password = Optional(str, 10, nullable=True, default=None)
    status = Required(str, 32)
    minplayers = Required(int)
    maxplayers = Required(int)
    numgames = Required(int)
    numrondas = Required(int)
    participante = Set(Robot, reverse='participa')
    creador = Required(Usuario, reverse='partida')
    ganador = Optional(Robot, reverse='gano')


db.generate_mapping(create_tables=True)
