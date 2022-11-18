from fastapi import APIRouter, HTTPException, status
from db import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class MatchResult:
    match_id: int
    name: str
    status: str
    numcurrentplayers: int
    minplayers: int
    maxplayers: int
    numgames: int
    numrounds: int
    creator: str
    password: bool


@router.get("/match/list",
            tags=["Match Methods"],
            name="List matches",
            response_model=List[MatchResult])
async def listar_partidas():
    with db_session:
        lista = [MatchResult(
            match_id=p.partida_id,
            name=p.namepartida,
            status=p.status,
            numcurrentplayers=len(p.participante),
            minplayers=p.minplayers,
            maxplayers=p.maxplayers,
            numgames=p.numgames,
            numrounds=p.numrondas,
            creator=p.creador.nombre_usuario,
            password=p.password is not None
        ) for p in Partida.select()]
    if lista == []:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No se encontraron partidas')
    return lista
