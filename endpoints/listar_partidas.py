from fastapi import APIRouter, HTTPException, status
from db import *

router = APIRouter()


@router.get("/lista_partidas")
async def listar_partidas(status_code=status.HTTP_200_OK):
    with db_session:
        lista = []
        for p in select(p for p in Partida):
            partida_datos = {
                'partida_id': p.partida_id,
                'partida_nombre': p.nombre,
                'partida.status': p.status,
                'partida_jugadores': len(p.participante),
                'partida_total_jugadores': p.cant_jugadores,
                'partida_juegos': p.cant_juegos,
                'partida_rondas': p.cant_rondas,
                'partida_creador': p.creador.nombre_usuario,
                'contraseña': p.contraseña is not None
            }
            lista.append(partida_datos)
        if lista == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron partidas')
        return lista
