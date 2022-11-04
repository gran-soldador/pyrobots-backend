from fastapi import APIRouter, HTTPException, status
from db import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class MatchResult:
    partida_id: int
    namepartida: str
    status: str
    numcurrentplayers: int
    minplayers: int
    maxplayers: int
    numgames: int
    numrondas: int
    creador: str
    password: bool


@router.get("/lista-partidas",
            tags=["Match Methods"],
            name="Lista de partidas",
            response_model=List[MatchResult])
async def listar_partidas():
    with db_session:
        lista = [MatchResult(
            partida_id=p.partida_id,
            namepartida=p.namepartida,
            status=p.status,
            numcurrentplayers=len(p.participante),
            minplayers=p.minplayers,
            maxplayers=p.maxplayers,
            numgames=p.numgames,
            numrondas=p.numrondas,
            creador=p.creador.nombre_usuario,
            password=p.password is not None
        ) for p in Partida.select()]
    if lista == []:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No se encontraron partidas')
    return lista
