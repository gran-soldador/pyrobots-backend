from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Query, Form
from .functions_jwt import *
import engine
from db import *


router = APIRouter()


@router.get("/simulacion")
async def estado_juego():
    try:
        return engine.run_demo_game()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='error en la simulación')

@router.post("/create_simulation")
async def simulation(user_id: int = Depends(authenticated_user),
                     rounds: int = Form(...),
                     robot_ids: List[int] = Query(...)
                    ):
    with db_session:
        if len(robot_ids) > 4:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='too many robots')
        elif len(robot_ids) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='not enough robots, at least 2 must be selected')
        elif rounds > 10000 or rounds <1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='the number of rounds must be between 1 and 10000')
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