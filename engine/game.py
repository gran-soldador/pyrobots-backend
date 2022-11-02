import logging
import random
from typing import Any, Generator, List, Tuple
from itertools import combinations  # hit calculation
from math import ceil               # missile flight delay

import heapq                        # missiles_in_flight data structure

from .robot import Robot, MisbehavingRobotException
from .vector import Vector
from .missile import MissileInFlight
from .constants import MAXX, MAXY, HITBOX, MISSILE_SPEED, MAXROUNDS
from .outputmodels import *


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
                        RobotStatus(x=pos.x, y=pos.y,
                                    damage=min(r._status.damage, 100)))
                missiles_status = []
                for m in self.missiles_in_flight:
                    pos = m.curr_pos(self.round)
                    missiles_status.append(
                        MissileStatus(x=pos.x, y=pos.y, angle=m.angle,
                                      sender=m.sender))
                explosions_status = [
                    ExplosionStatus(x=e.x, y=e.y) for e in self.explosions]
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
                **ret.args[0].__dict__  # MatchResult
            )

    def match(self) -> MatchResult:
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
                        shot_vec.angle,
                        r._status.id
                    )
                    heapq.heappush(self.missiles_in_flight, missile)
            self.explosions.clear()
            while (len(self.missiles_in_flight) > 0 and
                   self.missiles_in_flight[0].hit_round - 1 <= self.round):
                missile = heapq.heappop(self.missiles_in_flight)
                explosion = missile.destination
                for r in self.alive:  # pragma: no cover
                    distance = r._status.position.distance(explosion)
                    if distance < 5:
                        r._status.damage += 10
                    elif distance < 20:
                        r._status.damage += 5
                    elif distance < 40:
                        r._status.damage += 3
                self.explosions.append(explosion)

            for r in self.alive:
                others = [other._status.position
                          for other in self.alive if other is not r]
                r._execute_scanner(others)

            for r in self.alive:
                Robot._execute_drive(r)
            for r1, r2 in combinations(self.alive, 2):
                if (r1._status.position - r2._status.position).modulo < HITBOX:
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
