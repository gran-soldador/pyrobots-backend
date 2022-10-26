from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *

router = APIRouter()


@router.post('/unir-partida')
async def unir_partida(user_id: int = Depends(authenticated_user),
                       partida_id: int = Form(...),
                       contraseña: str = Form(None),
                       id_robot: int = Form(...)):
    with db_session:
        try:
            partida = Partida[partida_id]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if (partida.password) and partida.password != contraseña:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='contraseña incorrecta')
        if user_id == partida.creador.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='no puede unirse a su propia partida')
        for r in list(partida.participante):
            if r.usuario.user_id == user_id:
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
        return {'detail': 'unido exitosamente'}
