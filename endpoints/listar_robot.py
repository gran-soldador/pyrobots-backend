from fastapi import APIRouter, HTTPException, status, Depends
from db import *
from .functions_jwt import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class RobotResult:
    id: int
    name: str
    avatar: str
    played: int
    won: int
    avg_rounds: int


@router.get("/robot/list",
            tags=['Robot Methods'],
            name='List user robots',
            response_model=List[RobotResult])
async def list_robots(user_id: int = Depends(authenticated_user)):
    with db_session:
        robots = [RobotResult(id=r.id, name=r.name,
                              avatar="http://localhost:9000/" + r.avatar,
                              played=r.matches_num_played,
                              won=r.matches_num_won,
                              games=r.games_won,
                              rounds=r.rounds_won,
                              avg_rounds=r.rounds_won / r.games_won if
                              r.games_won != 0 else 0)
                  for r in User[user_id].robot]
        # TODO: Get static file server URL from env
        if robots == []:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='No se encontraron robots')
    return robots
