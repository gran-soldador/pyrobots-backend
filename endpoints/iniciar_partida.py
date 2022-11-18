from fastapi import APIRouter, Form, status, HTTPException, Depends
from fastapi import BackgroundTasks
from db import *
from .functions_jwt import *
from websocket import lobby_manager
from typing import Tuple, List, Dict
from engine import Game
from fastapi.concurrency import run_in_threadpool

router = APIRouter()


def loop(scores: Dict[int, int],
         rounds: Dict[int, int],
         robots: List[Tuple[int, str, str]],
         num_games: int, num_rounds: int):
    for game in range(num_games):
        match = Game(robots, num_rounds)
        result = match.match()
        for winner in result.winners:
            rounds[winner.id] += result.rounds_played
            scores[winner.id] += 1
    return rounds, scores


async def calculate_match(match_id: int, robots: List[Tuple[int, str, str]],
                          num_games: int, num_rounds: int):
    scores: Dict[int, int] = {}
    rounds: Dict[int, int] = {}
    for (robot_id, _, _) in robots:
        rounds[robot_id] = 0
        scores[robot_id] = 0
    rounds, scores = await run_in_threadpool(loop, scores, rounds,
                                             robots, num_games,
                                             num_rounds)
    max_points = max(scores, key=scores.get)
    with db_session:
        match = Match[match_id]
        for robot_id in scores:
            robot = Robot.get_for_update(id=robot_id)
            if scores[robot_id] == scores[max_points]:
                robot.matches_num_won += 1
                robot.games_won += scores[max_points]
                robot.rounds_won += rounds[max_points]
                match.winner.add(robot)
            robot.matches_num_played += 1
            robot.flush()
        match.status = 'finalizada'
        match.flush()
    await lobby_manager.broadcast(match_id, 'finish')


@router.post('/match/start',
             tags=["Match Methods"],
             name="Start match")
async def init_match(user_id: int = Depends(authenticated_user),
                     match_id: int = Form(...),
                     background_tasks: BackgroundTasks = BackgroundTasks()):
    with db_session:
        match = Match.get_for_update(id=match_id)
        if match is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if match.owner.id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='permiso denegado')
        if len(match.players) < match.min_players:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='jugadores insuficientes')
        if match.status not in ['disponible', 'ocupada']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida ya fue iniciada')
        robots = [(r.id, r.name, r.code) for r in match.players]
        background_tasks.add_task(calculate_match, match_id, robots,
                                  match.num_games, match.num_rounds)
        match.status = 'iniciada'
        match.flush()
    await lobby_manager.broadcast(match_id, 'init')
