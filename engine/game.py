from math import ceil
from .robot import Robot, MisbehavingRobotException
from .vector import Vector
from .missile import MissileInFlight
from .constants import MAXX, MAXY, HITBOX, MISSILE_SPEED
from typing import Any, Dict, Generator, List, Tuple
import logging
import random
from itertools import combinations
import heapq
from pydantic import BaseModel


# These COULD be dataclasses, as we don't need validation. But we know we are
# inside a REST API, and using a model eases auto generating docs
class RobotId(BaseModel):
    id: int
    name: str


class RobotRoundResult(BaseModel):
    x: float
    y: float
    damage: float


class RobotResult(RobotId):
    statuses: List[RobotRoundResult] = []


class MatchResult(BaseModel):
    rounds_played: int
    winners: List[RobotId]


class SimulationResult(BaseModel):
    maxrounds: int
    robots: List[RobotResult]


class Game:
    def __init__(self,
                 robot_descriptions: List[Tuple[int, str, str]],
                 rounds: int = 100000):
        assert 2 <= len(robot_descriptions) <= 4
        assert 1 <= rounds <= 100000
        logging.getLogger(__name__).debug("starting game")
        self.rounds = rounds
        self.robots: List[Robot] = []
        for num, (robot_id, name, code) in enumerate(robot_descriptions):
            try:
                exec(code)
                robot = eval(name)()
                if not isinstance(robot, Robot):
                    raise MisbehavingRobotException()
            except Exception:
                logging.getLogger(__name__).debug(
                    "Robot failed during construction", exc_info=True)
                robot = Robot()
                robot._status.damage = 100
            robot._status.position = Vector(cartesian=(
                random.uniform(.1, .9) * MAXX,
                random.uniform(.1, .9) * MAXY))
            robot._status.name = name
            robot._status.robot_id = robot_id
            robot._status.id = num
            self.robots.append(robot)

    @property
    def alive(self) -> List[Robot]:
        return [r for r in self.robots if r._status.damage < 100]

    def simulation(self) -> Dict[str, Any]:
        result = SimulationResult(
            maxrounds=self.rounds,
            robots=[RobotResult(id=r._status.robot_id, name=r._status.name)
                    for r in self.robots]
        )

        self._initialize_robots()
        round_generator = self._execute_rounds()
        try:
            while True:
                for (game_r, out_r) in zip(self.robots, result.robots):
                    curr_status = RobotRoundResult(
                        x=game_r._status.position.x,
                        y=game_r._status.position.y,
                        damage=game_r._status.damage
                    )
                    out_r.statuses.append(curr_status)
                # TODO: Add missiles in flight to result
                next(round_generator)
        except StopIteration as ret:
            return result.dict() | ret.args[0].dict()

    def match(self) -> Tuple[int, int, str]:
        self._initialize_robots()
        round_generator = self._execute_rounds()
        try:
            while True:
                next(round_generator)
        except StopIteration as ret:
            return ret.args[0]  # rounds played, winner id and name

    def _initialize_robots(self):
        for r in self.alive:
            Robot._initialize_or_die(r)

    def _execute_rounds(self) -> Generator[Any, None, MatchResult]:
        # TODO: REFACTOR! Divide into cannon, scanner and movement stages.
        round = 0
        missiles_in_flight: List[MissileInFlight] = []
        while len(self.alive) > 1 and round < self.rounds:
            for r in self.alive:
                Robot._respond_or_die(r)

            for r in self.alive:
                if (shot_vec := Robot._execute_cannon(r)) is not None:
                    missile = MissileInFlight(
                        round + ceil(shot_vec.modulo / MISSILE_SPEED),
                        round,
                        r._status.position,
                        r._status.position + shot_vec,
                        shot_vec.angle
                    )
                    heapq.heappush(missiles_in_flight, missile)
            while (len(missiles_in_flight) > 0 and
                   missiles_in_flight[0].hit_round <= round):
                missile = heapq.heappop(missiles_in_flight)
                explosion = missile.destination
                for r in self.alive:
                    distance = r._status.position.distance(explosion)
                    if distance < 100:
                        logging.getLogger(__name__).debug(
                            f"\t{round} -> exploded! near {r._status.name}")
                    # TODO: Calculate damage

            for r in self.alive:
                Robot._execute_drive(r)
            for r1, r2 in combinations(self.alive, 2):
                if Robot._get_distance(r1, r2) < HITBOX:
                    r1._status.damage += 2
                    r2._status.damage += 2

            round += 1
            yield
        return MatchResult(
            rounds_played=round,
            winners=[RobotId(id=r._status.robot_id, name=r._status.name)
                     for r in self.alive]
        )
