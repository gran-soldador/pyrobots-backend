from fastapi import APIRouter, HTTPException, status, Depends
from db import *
from .functions_jwt import *

router = APIRouter()


@router.get("/lista-robots")
async def listar_robots(user_id: int = Depends(authenticated_user)):
    with db_session:
        lista = [{'id': r.robot_id, 'nombre': r.nombre}
                 for r in Usuario[user_id].robot]
        if lista == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron robots')
        return lista
