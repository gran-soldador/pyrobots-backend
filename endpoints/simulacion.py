from fastapi import APIRouter, status, HTTPException, Depends, Form
from .functions_jwt import *
import engine
from db import *


router = APIRouter()


@router.post("/create_simulation")
async def simulation(user_id: int = Depends(authenticated_user),
                     rounds: int = Form(...),
                     robot_ids: list = Form(...)
                     ):
    robot_ids = robot_ids[0].split(",")
    with db_session:
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
        for i in robot_ids:
            if Robot.get(robot_id=i) is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='Robot does not exist')
        try:
            list_robot = []
            for r in robot_ids:
                robot = (r, Robot.get(robot_id=r).nombre,
                         Robot.get(robot_id=r).implementacion,
                         )
                list_robot.append(tuple(robot))
            return engine.Game(list_robot, rounds).simulation()
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='error en la simulación')
