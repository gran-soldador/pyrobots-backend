from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *
from websocket import lobby_manager

router = APIRouter()


@router.post('/match/exit',
             tags=["Match Methods"],
             name="Exit joined match")
async def exit_match(user_id: int = Depends(authenticated_user),
                     match_id: int = Form(...)):
    with db_session:
        match = Match.get_for_update(id=match_id)
        if match is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        user = list(match.players)
        user = list(filter(lambda r: r.user.id == user_id, user))
        if user == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='no es un participante')
        if match.owner.id == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el creador no puede abandonar')
        if match.status not in ['disponible', 'ocupada']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='ya no tiene permitido abandonar')
        match.players.remove(user)
        match.flush()
        match.status = 'disponible'
    await lobby_manager.broadcast(match_id, 'quit')
