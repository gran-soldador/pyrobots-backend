from fastapi import APIRouter, HTTPException, status
from db import *
from dataclasses import dataclass
from typing import List

router = APIRouter()


@dataclass(slots=True)
class MatchResult:
    match_id: int
    name: str
    status: str
    numcurrentplayers: int
    minplayers: int
    maxplayers: int
    numgames: int
    numrounds: int
    creator: str
    password: bool


@router.get("/match/list",
            tags=["Match Methods"],
            name="List matches",
            response_model=List[MatchResult])
async def list_matches():
    with db_session:
        matches = [MatchResult(
            match_id=p.id,
            name=p.name,
            status=p.status,
            numcurrentplayers=len(p.players),
            minplayers=p.min_players,
            maxplayers=p.max_players,
            numgames=p.num_games,
            numrounds=p.num_rounds,
            creator=p.owner.name,
            password=p.password is not None
        ) for p in Match.select()]
    if matches == []:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='No se encontraron partidas')
    return matches
