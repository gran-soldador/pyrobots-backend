from fastapi import APIRouter, status
from db import *
import json

router = APIRouter()


@router.get("/lista_partidas")
async def listar_partidas():
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
                'partida_creador': p.creador.nombre_usuario
            }
            lista.append(partida_datos)
        if lista == []:
            return (status.HTTP_400_BAD_REQUEST,
                    json.dumps({'type': 'no se encontraron resultados'}))
        return (status.HTTP_200_OK, json.dumps(lista))


@router.get('/test_lista')
async def test_lista():
    with db_session:
        u1 = Usuario(nombre_usuario='juan', email='juan.lopez@mi.unc.edu.ar',
                     contraseña='@Leandro013', verificado=True)
        p1 = Partida(nombre='partida', status='disponible', cant_jugadores=3,
                     cant_juegos=10, cant_rondas=10, creador=u1)
        p1.flush()
        id_partida = p1.partida_id
        return {'status': '200 ok', 'id_partida': id_partida}
