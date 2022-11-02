from fastapi import APIRouter, status, HTTPException, Depends, Form
from .functions_jwt import *
import engine
from db import *


router = APIRouter()


@router.post("/create_simulation")
async def simulation(user_id: int = Depends(authenticated_user),
                     rounds: int = Form(...),
                     robot_ids: str = Form(...)  # comma separated list
                     ):
    try:
        robot_ids = [int(id) for id in robot_ids.split(",")]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='invalid robot list') from e
    if len(robot_ids) > 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='too many robots')
    elif len(robot_ids) < 2:
        detail = 'not enough robots, at least 2 must be selected'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)
    elif rounds > 10000 or rounds < 1:
        detail = 'the number of rounds must be between 1 and 10000'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=detail)
    with db_session:
        robots = []
        for id in robot_ids:
            robot = Robot.get(robot_id=id)
            if robot is None or robot.usuario.user_id != user_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='Robot does not exist')
            robots.append((id, robot.nombre, robot.implementacion))
    try:
        return engine.Game(robots, rounds).simulation()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Simulation error')
