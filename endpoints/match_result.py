from fastapi import APIRouter, Form, status, HTTPException
from db import *
from .functions_jwt import *

router = APIRouter()


@router.post('/match-result')
async def return_result(partida_id: int = Form(...)):
    with db_session:
        try:
            partida = Partida[partida_id]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if partida.status != 'finalizada':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no tiene resultados')
        ganador = [u.usuario.nombre_usuario for u in partida.ganador]
        return {'ganador': ganador}
