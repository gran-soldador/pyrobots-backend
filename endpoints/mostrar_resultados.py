from fastapi import APIRouter, status, HTTPException
from db import *
from .functions_jwt import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class WinnerResult:
    usuario: str
    robot: str
    id: int


@router.get('/mostrar-resultados/{partida_id}',
            tags=["Match Methods"],
            name="Resultados de partida",
            response_model=List[WinnerResult])
async def return_result(partida_id: int):
    with db_session:
        partida = Partida.get(partida_id=partida_id)
        if partida is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if partida.status != 'finalizada':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no tiene resultados')
        ganador = [WinnerResult(
                   usuario=u.usuario.nombre_usuario,
                   robot=u.nombre,
                   id=u.usuario.user_id
                   ) for u in partida.ganador]
        return ganador
