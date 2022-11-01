from fastapi import APIRouter, Form, status, HTTPException, Depends
from fastapi import BackgroundTasks
from db import *
from .functions_jwt import *
from websocket import lobby_manager
from typing import Tuple, List, Dict
from engine import Game
from fastapi.concurrency import run_in_threadpool

router = APIRouter()


def loop(scores: Dict[int, int], robots: List[Tuple[int, str, str]],
         numgames: int, numrondas: int):
    for game in range(numgames):
        match = Game(robots, numrondas)
        winner = match.match()
        try:
            scores[winner[1]] += 1
        except Exception:
            pass
    return scores


async def calculate_match(partida_id: int, robots: List[Tuple[int, str, str]],
                          numgames: int, numrondas: int):
    scores: Dict[int, int] = {}
    for (robot_id, _, _) in robots:
        scores[robot_id] = 0
    scores = await run_in_threadpool(loop, scores, robots, numgames, numrondas)
    max_points = max(scores, key=scores.get)
    with db_session:
        partida = Partida[partida_id]
        for robot_id in scores:
            robot = Robot[robot_id]
            if scores[robot_id] == scores[max_points]:
                robot.partidas_ganadas += 1
                partida.ganador.add(robot)
            robot.partidas_jugadas += 1
            robot.flush()
        partida.status = 'finalizada'
        partida.flush()
    await lobby_manager.broadcast(partida_id, 'finish')


@router.post('/iniciar-partida')
async def init_match(user_id: int = Depends(authenticated_user),
                     partida_id: int = Form(...),
                     background_tasks: BackgroundTasks = BackgroundTasks()):
    with db_session:
        partida = Partida.get_for_update(partida_id=partida_id)
        if partida is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida no existe')
        if partida.creador.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='permiso denegado')
        if len(partida.participante) < partida.minplayers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='jugadores insuficientes')
        if partida.status not in ['disponible', 'ocupada']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='la partida ya fue iniciada')
        robots = [(r.robot_id, r.nombre, r.implementacion) for r in
                  partida.participante]
        background_tasks.add_task(calculate_match, partida_id, robots,
                                  partida.numgames, partida.numrondas)
        partida.status = 'iniciada'
        partida.flush()
    await lobby_manager.broadcast(partida_id, 'init')
    return {'detail': partida.status}
