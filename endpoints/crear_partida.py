from fastapi import APIRouter, Form, status, HTTPException
from db import *
import string

router = APIRouter()

VALID_CHAR = (string.ascii_lowercase + string.ascii_uppercase
              + ''.join([str(i) for i in range(0, 10)]) + '-_'
              )


def check_string(string: str) -> bool:
    for i in string:
        if i not in VALID_CHAR:
            return False
    return True


@router.post("/crear-partida")
async def crear_partida(namepartida: str = Form(...),
                        password: str = Form(None),
                        numplayers: int = Form(...),
                        numgames: int = Form(...),
                        numrondas: int = Form(...),
                        idrobot: int = Form(...),
                        status_code=status.HTTP_200_OK):
    if (len(namepartida) <= 32 and check_string(namepartida)) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='namepartida invalido')
    if password:
        if (len(password) <= 10 and check_string(password)) is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='password invalida')
    if (numplayers >= 2 and numplayers <= 4) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='numplayers invalido')
    if (numgames >= 1 and numgames <= 200) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='numgames invalido')
    if (numrondas >= 1 and numrondas <= 10000) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='numrondas invalido')
    with db_session:
        try:
            robot = Robot[idrobot]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='robot no valido')
        if robot.defectuoso is True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='robot defectuoso')
        if password:
            p1 = Partida(namepartida=namepartida, password=password,
                         status='disponible',
                         numplayers=numplayers,
                         numgames=numgames,
                         numrondas=numrondas,
                         creador=robot.usuario)
        else:
            p1 = Partida(namepartida=namepartida,
                         status='disponible',
                         numplayers=numplayers,
                         numgames=numgames,
                         numrondas=numrondas,
                         creador=robot.usuario)
        p1.participante.add(robot)
        p1.flush()
        partida_id = p1.partida_id
        return {'id_partida': partida_id}