from fastapi import APIRouter, status, HTTPException
from db import *
from .functions_jwt import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class WinnerResult:
    user: str
    robot: str
    id: int


@router.get('/match/results/{match_id}',
            tags=["Match Methods"],
            name="Match results",
            response_model=List[WinnerResult])
async def return_result(match_id: int):
    with db_session:
        partida = Partida.get(partida_id=match_id)
        if partida is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if partida.status != 'finalizada':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no tiene resultados')
        ganador = [WinnerResult(
                   user=u.usuario.nombre_usuario,
                   robot=u.nombre,
                   id=u.usuario.user_id
                   ) for u in partida.ganador]
        return ganador
