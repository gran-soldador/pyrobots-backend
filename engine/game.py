import logging
import random
from typing import Any
from collections.abc import Generator
from itertools import combinations  # hit calculation
from math import ceil

from .constants import MAXX, MAXY, HITBOX, MISSILE_SPEED, MAXROUNDS
from .heap import Heap
from .missile import MissileInFlight
from .outputmodels import *
from .robot import Robot, MisbehavingRobotException
from .vector import Vector


class Game:
    def __init__(self,
                 robot_descriptions: list[tuple[int, str, str]],
                 rounds: int = MAXROUNDS):
        assert 2 <= len(robot_descriptions) <= 4
        assert 1 <= rounds <= MAXROUNDS
        logging.getLogger(__name__).debug("starting game")
        self.maxrounds = rounds
        self.round = 0
        self.robots: list[Robot] = []
        self.missiles_in_flight: Heap[MissileInFlight] = Heap()
        self.explosions: list[Vector] = []
        for num, (robot_id, name, code) in enumerate(robot_descriptions):
            position = (random.uniform(.1, .9) * MAXX,
                        random.uniform(.1, .9) * MAXY)
            damage = 0
            try:
                exec(code)
                robotClass = eval(name)
                if not issubclass(robotClass, Robot):
                    raise MisbehavingRobotException()
            except Exception:
                logging.getLogger(__name__).debug(
                    "Robot failed during construction", exc_info=True)
                robotClass = Robot
                damage = 100
            robot = robotClass(num, name, robot_id, position, damage)
            self.robots.append(robot)

    @property
    def alive(self) -> list[Robot]:
        return [r for r in self.robots if r.get_damage() < 100]

    def simulation(self) -> SimulationResult:
        rounds = []
        round_generator = self._execute_rounds()
        try:
            while True:
                # Gather data
                robots_status = []
                for r in self.robots:
                    x, y = r.get_position()
                    scanner = ScannerStatus(*r._get_scanner_command())
                    robots_status.append(
                        RobotStatus(x=x, y=y, damage=min(r.get_damage(), 100),
                                    scanner=scanner))
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
            match_result = ret.args[0]
        return SimulationResult(
            maxrounds=self.maxrounds, rounds=rounds,
            **match_result.__dict__
        )

    def match(self) -> MatchResult:
        round_generator = self._execute_rounds()
        try:
            while True:
                next(round_generator)
        except StopIteration as ret:
            return ret.args[0]  # rounds played, winner id and name

    def _execute_rounds(self) -> Generator[Any, None, MatchResult]:
        self._initialize_robots()
        while len(self.alive) > 1 and self.round < self.maxrounds:
            for r in self.alive:
                r._respond_or_die()
            self._execute_cannons()
            self._execute_scanners()
            self._execute_drives()
            self.round += 1
            yield
        return MatchResult(
            rounds_played=self.round,
            players=[RobotId(id=r._status.robot_id, name=r._status.name)
                     for r in self.robots],
            winners=[RobotId(id=r._status.robot_id, name=r._status.name)
                     for r in self.alive]
        )

    def _initialize_robots(self):
        for r in self.alive:
            Robot._initialize_or_die(r)

    def _execute_cannons(self):
        for r in self.alive:
            if (shot_vec := r._execute_cannon()) is not None:
                pos = r._get_position_vec()
                missile = MissileInFlight(
                    self.round + ceil(shot_vec.modulo / MISSILE_SPEED),
                    self.round,
                    pos,
                    pos + shot_vec,
                    shot_vec.angle,
                    r._get_id()
                )
                self.missiles_in_flight.push_back(missile)
        self.explosions.clear()
        while (len(self.missiles_in_flight) > 0 and
               self.missiles_in_flight.front().hit_round - 1 <= self.round):
            missile = self.missiles_in_flight.pop_front()
            explosion = missile.destination
            for r in self.alive:
                distance = r._get_position_vec().distance(explosion)
                if distance < 5:
                    r._apply_damage(10)
                elif distance < 20:
                    r._apply_damage(5)
                elif distance < 40:
                    r._apply_damage(3)
            self.explosions.append(explosion)

    def _execute_scanners(self):
        for r in self.alive:
            others = [other._get_position_vec()
                      for other in self.alive if other is not r]
            r._execute_scanner(others)

    def _execute_drives(self):
        for r in self.alive:
            r._execute_drive()
        for r1, r2 in combinations(self.alive, 2):
            distance = (r1._get_position_vec() - r2._get_position_vec()).modulo
            if distance < HITBOX:
                r1._apply_damage(2)
                r2._apply_damage(2)
