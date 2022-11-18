from fastapi import APIRouter, Form, status, HTTPException, Depends
from db import *
from utils.tokens import *
import string
from websocket import lobby_manager

router = APIRouter()

VALID_CHAR = (string.ascii_letters + string.digits + '-_')


def check_string(string: str) -> bool:
    return all(c in VALID_CHAR for c in string)


@router.post("/match/new",
             tags=["Match Methods"],
             name="Create a new match")
async def new_match(user_id: int = Depends(authenticated_user),
                    name: str = Form(...),
                    password: str = Form(None),
                    minplayers: int = Form(...),
                    maxplayers: int = Form(...),
                    numgames: int = Form(...),
                    numrounds: int = Form(...),
                    robot_id: int = Form(...)):
    match_id = None
    if (len(name) <= 32 and check_string(name)) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='namepartida invalido')
    if password:
        if (len(password) <= 10 and check_string(password)) is False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='password invalida')
    if (minplayers >= 2 and minplayers <= maxplayers <= 4) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='minplayers o maxplayers invalido')
    if (numgames >= 1 and numgames <= 200) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='numgames invalido')
    if (numrounds >= 1 and numrounds <= 10000) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='numrondas invalido')
    with db_session:
        robot = Robot.get(id=robot_id)
        if robot is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='robot no valido')
        if robot.user.id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="robot no pertenece al usuario")
        if robot.defective is True:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='robot defectuoso')
        p1 = Match(name=name, password=password,
                   status='disponible',
                   min_players=minplayers,
                   max_players=maxplayers,
                   num_games=numgames,
                   num_rounds=numrounds,
                   owner=robot.user)
        p1.players.add(robot)
        p1.flush()
        match_id = p1.id
    await lobby_manager.broadcast(match_id, 'created')
