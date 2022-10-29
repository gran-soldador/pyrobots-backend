from math import ceil
from .robot import Robot, MisbehavingRobotException
from .vector import Vector
from .missile import MissileInFlight
from .constants import MAXX, MAXY, HITBOX, MISSILE_SPEED, MAXROUNDS
from typing import Any, Generator, List, Tuple
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


class Status(BaseModel):
    x: float
    y: float


class RobotStatus(Status):
    damage: float


class MissileStatus(Status):
    angle: float


class ExplosionStatus(Status):
    pass


class RoundResult(BaseModel):
    robots: List[RobotStatus]
    missiles: List[MissileStatus] = []
    explosions: List[ExplosionStatus] = []


class MatchResult(BaseModel):
    rounds_played: int
    players: List[RobotId]
    winners: List[RobotId]


class SimulationResult(MatchResult):
    maxrounds: int
    rounds: List[RoundResult]


class Game:
    def __init__(self,
                 robot_descriptions: List[Tuple[int, str, str]],
                 rounds: int = MAXROUNDS):
        assert 2 <= len(robot_descriptions) <= 4
        assert 1 <= rounds <= MAXROUNDS
        logging.getLogger(__name__).debug("starting game")
        self.maxrounds = rounds
        self.round = 0
        self.robots: List[Robot] = []
        self.missiles_in_flight: List[MissileInFlight] = []
        self.explosions: List[Vector] = []
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

    def simulation(self) -> SimulationResult:
        rounds = []
        self._initialize_robots()
        round_generator = self._execute_rounds()
        try:
            while True:
                # Gather data
                robots_status = []
                for r in self.robots:
                    pos = r._status.position
                    robots_status.append(
                        RobotStatus(x=pos.x, y=pos.y, damage=r._status.damage))
                missiles_status = []
                for m in self.missiles_in_flight:
                    pos = m.curr_pos(self.round)
                    missiles_status.append(
                        MissileStatus(x=pos.x, y=pos.y, angle=m.angle))
                explosions_status = [
                    ExplosionStatus(x=e.x, y=e.y) for e in self.explosions]
                self.explosions.clear()  # Delete explosions for next round
                # Add to result
                rounds.append(
                    RoundResult(robots=robots_status,
                                missiles=missiles_status,
                                explosions=explosions_status))
                # Done, now advance
                next(round_generator)
        except StopIteration as ret:
            return SimulationResult(
                maxrounds=self.maxrounds, rounds=rounds,
                **dict(ret.args[0])  # MatchResult
            )

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
        while len(self.alive) > 1 and self.round < self.maxrounds:
            for r in self.alive:
                Robot._respond_or_die(r)

            for r in self.alive:
                if (shot_vec := Robot._execute_cannon(r)) is not None:
                    missile = MissileInFlight(
                        self.round + ceil(shot_vec.modulo / MISSILE_SPEED),
                        self.round,
                        r._status.position,
                        r._status.position + shot_vec,
                        shot_vec.angle
                    )
                    heapq.heappush(self.missiles_in_flight, missile)
            while (len(self.missiles_in_flight) > 0 and
                   self.missiles_in_flight[0].hit_round <= self.round):
                missile = heapq.heappop(self.missiles_in_flight)
                explosion = missile.destination
                for r in self.alive:
                    distance = r._status.position.distance(explosion)
                    distance = distance
                    # TODO: Calculate damage
                self.explosions.append(explosion)

            for r in self.alive:
                Robot._execute_drive(r)
            for r1, r2 in combinations(self.alive, 2):
                if Robot._get_distance(r1, r2) < HITBOX:
                    r1._status.damage += 2
                    r2._status.damage += 2

            self.round += 1
            yield
        return MatchResult(
            rounds_played=self.round,
            players=[RobotId(id=r._status.robot_id, name=r._status.name)
                     for r in self.robots],
            winners=[RobotId(id=r._status.robot_id, name=r._status.name)
                     for r in self.alive]
        )
