from fastapi import APIRouter, HTTPException, status, Depends
from db import *
from .functions_jwt import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class RobotResult:
    id: int
    nombre: str
    avatar: str


@router.get("/lista-robots",
            tags=['Robot Methods'],
            name='lista los robots del usuario',
            response_model=List[RobotResult])
async def listar_robots(user_id: int = Depends(authenticated_user)):
    with db_session:
        lista = [RobotResult(id=r.robot_id, nombre=r.nombre,
                 avatar="http://0.0.0.0:9000/" + r.avatar)
                 for r in Usuario[user_id].robot]
        if lista == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron robots')
    return lista
