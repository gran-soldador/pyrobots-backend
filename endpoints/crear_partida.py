from fastapi import APIRouter, Form, status, HTTPException
from db import *
import string

router = APIRouter()

char = string.ascii_lowercase
char += string.ascii_uppercase
char += ''.join([str(i) for i in range(0, 10)])
char += '-_'


def check_string(string: str) -> bool:
    for i in string:
        if i not in char:
            return False
    return True


@router.post("/crear_partida")
async def crear_partida(nombre: str = Form(...),
                        contraseña: str = Form(None),
                        cant_jugadores: int = Form(...),
                        cant_juegos: int = Form(...),
                        cant_rondas: int = Form(...),
                        robot_id: int = Form(...),
                        status_code=status.HTTP_200_OK):
    if (len(nombre) <= 32 and check_string(nombre)) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='nombre invalido')
    if contraseña:
        if (len(contraseña) <= 10 and check_string(contraseña)) is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='contraseña invalida')
    if (cant_jugadores >= 2 and cant_jugadores <= 4) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='número de jugadores invalido')
    if (cant_juegos >= 1 and cant_juegos <= 200) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='número de juegos invalido')
    if (cant_rondas >= 1 and cant_rondas <= 200) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='número de rondas invalido')
    with db_session:
        try:
            robot = Robot[robot_id]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='robot no valido')
        if robot.defectuoso is True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='robot defectuoso')
        if contraseña:
            p1 = Partida(nombre=nombre, contraseña=contraseña,
                         status='disponible',
                         cant_jugadores=cant_jugadores,
                         cant_juegos=cant_juegos,
                         cant_rondas=cant_rondas,
                         creador=robot.usuario)
        else:
            p1 = Partida(nombre=nombre,
                         status='disponible',
                         cant_jugadores=cant_jugadores,
                         cant_juegos=cant_juegos,
                         cant_rondas=cant_rondas,
                         creador=robot.usuario)
        p1.participante.add(robot)
        p1.flush()
        partida_id = p1.partida_id
        return {'id_partida': partida_id}
