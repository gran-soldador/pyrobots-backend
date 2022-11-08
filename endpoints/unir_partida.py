from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *
from websocket import lobby_manager

router = APIRouter()


@router.post('/match/join',
             tags=["Match Methods"],
             name="Join a match")
async def unir_partida(user_id: int = Depends(authenticated_user),
                       match_id: int = Form(...),
                       password: str = Form(None),
                       robot_id: int = Form(...)):
    with db_session:
        partida = Partida.get_for_update(partida_id=match_id)
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
        robot = Robot.get(robot_id=robot_id)
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
    await lobby_manager.broadcast(match_id, 'join')
