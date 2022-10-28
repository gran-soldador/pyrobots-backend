from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *
from websocket import lobby_manager

router = APIRouter()


@router.post('/unir-partida')
async def unir_partida(user_id: int = Depends(authenticated_user),
                       partida_id: int = Form(...),
                       password: str = Form(None),
                       id_robot: int = Form(...)):
    with db_session:
        try:
            partida = Partida[partida_id]
        except Exception:
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
        try:
            robot = Robot[id_robot]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el robot no existe')
        if robot.usuario.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el robot no pertenece al usuario')
        partida.participante.add(robot)
        partida.flush()
        await lobby_manager.broadcast(
            partida_id,
            {
                "event": "created",
                "creador": Partida[partida_id].creador.nombre_usuario,
                "robot": [{"id": r.robot_id, "nombre": r.nombre,
                           "usuario": r.usuario.nombre_usuario} for r in
                          list(Partida[partida_id].participante)]
            }
        )
        if len(partida.participante) == partida.maxplayers:
            partida.status = 'ocupada'
        return {'detail': partida.status}
