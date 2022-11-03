from fastapi import APIRouter, status, HTTPException
from db import *
from .functions_jwt import *

router = APIRouter()


@router.get('/mostrar-resultados/{partida_id}',
            tags=["Match Methods"],
            name="Resultados de partida")
async def return_result(partida_id: int):
    with db_session:
        try:
            partida = Partida[partida_id]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if partida.status != 'finalizada':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no tiene resultados')
        ganador = [{
                   'usuario': u.usuario.nombre_usuario,
                   'robot': u.nombre,
                   'id': u.usuario.user_id
                   } for u in partida.ganador]
        return ganador
