from cattrs.preconf.json import make_converter
# TODO: Test other cattrs preconfs for performance
from fastapi import APIRouter, status, HTTPException, Depends, Form, Response

from db import *
import engine
from engine.outputmodels import SimulationResult
from utils.tokens import *


converter = make_converter()
router = APIRouter()


@router.post("/simulation",
             tags=['Simulation Methods'],
             name='Run simulation',
             response_model=SimulationResult)
async def simulation(user_id: int = Depends(authenticated_user),
                     rounds: int = Form(...),
                     robot_ids: list[int] = Form(...)
                     ):
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
            robot = Robot.get(id=id)
            if robot is None or robot.user.id != user_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='Robot does not exist')
            robots.append((id, robot.name, robot.code))
    try:
        result = engine.Game(robots, rounds).simulation()
        # We COULD do `return result`, but some quick measurements show that
        # is ~10 times slower.
        json_str = converter.dumps(result)
        return Response(json_str, media_type="application/json")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Simulation error')
