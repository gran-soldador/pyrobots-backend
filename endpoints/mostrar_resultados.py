from fastapi import APIRouter, status, HTTPException
from db import *
from utils.tokens import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class WinnerResult:
    user: str
    robot: str
    id: int


@router.get('/match/results/{match_id}',
            tags=["Match Methods"],
            name="Match results",
            response_model=List[WinnerResult])
async def return_result(match_id: int):
    with db_session:
        match = Match.get(id=match_id)
        if match is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if match.status != 'finalizada':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no tiene resultados')
        winner = [WinnerResult(
                  user=u.user.name,
                  robot=u.name,
                  id=u.user.id
                  ) for u in match.winner]
        return winner
