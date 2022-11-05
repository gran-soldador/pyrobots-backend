from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *
from websocket import lobby_manager

router = APIRouter()


@router.post('/unir-partida',
             tags=["Match Methods"],
             name="Unión a partida")
async def unir_partida(user_id: int = Depends(authenticated_user),
                       partida_id: int = Form(...),
                       password: str = Form(None),
                       id_robot: int = Form(...)):
    with db_session:
        partida = Partida.get_for_update(partida_id=partida_id)
        if partida is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if partida.status != 'disponible':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='partida no disponible')
        if partida.password != password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='contraseña incorrecta')
        if user_id == partida.creador.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='no puede unirse a su propia partida')
        user = list(partida.participante)
        user = list(filter(lambda r: r.usuario.user_id == user_id, user))
        if user != []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='usuario ya unido')
        robot = Robot.get(robot_id=id_robot)
        if robot is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el robot no existe')
        if robot.usuario.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el robot no pertenece al usuario')
        partida.participante.add(robot)
        partida.flush()
        if len(partida.participante) == partida.maxplayers:
            partida.status = 'ocupada'
    await lobby_manager.broadcast(partida_id, 'join')
