from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from .functions_jwt import *
from websocket import lobby_manager

router = APIRouter()


@router.post('/match/join',
             tags=["Match Methods"],
             name="Join a match")
async def match_join(user_id: int = Depends(authenticated_user),
                     match_id: int = Form(...),
                     password: str = Form(None),
                     robot_id: int = Form(...)):
    with db_session:
        match = Match.get_for_update(id=match_id)
        if match is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if match.status != 'disponible':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='partida no disponible')
        if match.password != password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='contraseña incorrecta')
        if user_id == match.owner.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='no puede unirse a su propia partida')
        user = list(match.players)
        user = list(filter(lambda r: r.user.id == user_id, user))
        if user != []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='usuario ya unido')
        robot = Robot.get(id=robot_id)
        if robot is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el robot no existe')
        if robot.user.id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='el robot no pertenece al usuario')
        match.players.add(robot)
        match.flush()
        if len(match.players) == match.max_players:
            match.status = 'ocupada'
    await lobby_manager.broadcast(match_id, 'join')
