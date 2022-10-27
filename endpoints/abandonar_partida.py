from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *
from websocket import lobby_manager
import asyncio

router = APIRouter()


@router.post('/abandonar-partida')
async def abandonar_partida(user_id: int = Depends(authenticated_user),
                            partida_id: int = Form(...)):
    with db_session:
        try:
            partida = Partida[partida_id]
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        user = list(partida.participante)
        user = list(filter(lambda r: r.usuario.user_id == user_id, user))
        if user == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='no es un participante')
        if partida.creador.user_id == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el creador no puede abandonar')
        if partida.status not in ['disponible', 'ocupada']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='ya no tiene permitido abandonar')
        partida.participante.remove(user)
        partida.flush()
        asyncio.gather(lobby_manager.broadcast(
            partida_id,
            {
                "event": "quit",
                "robots": [{"id": r.robot_id, "nombre": r.nombre}
                           for r in list(Partida[partida_id].participante)]
            }
        ))
        if len(partida.participante) < partida.maxplayers:
            partida.status = 'disponible'
        return {'detail': partida.status}
