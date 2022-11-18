from fastapi import APIRouter, HTTPException, status, Depends
from db import *
from .functions_jwt import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class RobotResult:
    id: int
    name: str
    avatar: str
    played: int
    won: int
    avg_rounds: int


@router.get("/robot/list",
            tags=['Robot Methods'],
            name='List user robots',
            response_model=List[RobotResult])
async def listar_robots(user_id: int = Depends(authenticated_user)):
    with db_session:
        lista = [RobotResult(id=r.robot_id, name=r.nombre,
                 avatar="http://localhost:9000/" + r.avatar,
                 played=r.partidas_jugadas,
                 won=r.partidas_ganadas,
                 games=r.juegos_ganados,
                 rounds=r.rondas_ganadas,
                 avg_rounds=r.rondas_ganadas / r.juegos_ganados if
                 r.juegos_ganados != 0 else 0)
                 for r in Usuario[user_id].robot]
        if lista == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron robots')
    return lista
