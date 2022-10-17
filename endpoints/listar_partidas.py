from fastapi import APIRouter, HTTPException, status
from db import *

router = APIRouter()


@router.get("/lista-partidas")
async def listar_partidas():
    with db_session:
        lista = []
        for p in select(p for p in Partida):
            partida_datos = {
                'partida_id': p.partida_id,
                'namepartida': p.namepartida,
                'status': p.status,
                'numcurrentplayers': len(p.participante),
                'minplayers': p.minplayers,
                'maxplayers': p.maxplayers,
                'numgames': p.numgames,
                'numrondas': p.numrondas,
                'creador': p.creador.nombre_usuario,
                'password': p.password is not None
            }
            lista.append(partida_datos)
        if lista == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron partidas')
        return lista
