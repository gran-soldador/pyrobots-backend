from .robot import Robot, Position, MAXX, MAXY, HITBOX
from typing import Any, Generator, List, Tuple
import logging
import random
from itertools import combinations


class Game:
    def __init__(self,
                 robot_descriptions: List[Tuple[str, str]],
                 rounds: int = 100000):
        assert 2 <= len(robot_descriptions) <= 4
        assert 1 <= rounds <= 100000
        logging.getLogger(__name__).debug("starting game")
        self.rounds = rounds
        self.robots: List[Robot] = []
        for num, (name, code) in enumerate(robot_descriptions):
            try:
                exec(code)
                robot = eval(name)()
                assert isinstance(robot, Robot)
            except Exception:
                logging.getLogger(__name__).debug(
                    "Robot failed during construction", exc_info=True)
                robot = Robot()
                robot._status.damage = 100
            robot._status.position = Position(
                random.uniform(.1, .9) * MAXX,
                random.uniform(.1, .9) * MAXY)
            robot._status.name = name
            robot._status.id = num
            self.robots.append(robot)

    @property
    def alive(self) -> List[Robot]:
        return [r for r in self.robots if r._status.damage < 100]

    def simulate(self):
        result = {
            "maxrounds": self.rounds,
            "robotcount": len(self.robots),
            "robots": [{
                "name": r._status.name,
                "positions": [],
                "damage": []
            } for r in self.robots]
        }

        self._initialize_robots()
        round_generator = self._execute_rounds()
        try:
            while True:
                for r in self.robots:
                    x = r._status.position.x
                    y = r._status.position.y
                    damage = r._status.damage
                    result["robots"][r._status.id]["positions"].append(
                        {"x": x, "y": y}
                    )
                    result["robots"][r._status.id]["damage"].append(damage)
                next(round_generator)
        except StopIteration as ret:
            result["rounds"], result["winner"] = ret.args[0]
        return result

    def _initialize_robots(self):
        for r in self.alive:
            Robot._initialize_or_die(r)

    def _execute_rounds(self) -> Generator[Any, None, Tuple[int, int]]:
        round = 0
        while len(self.alive) > 1 and round < self.rounds:
            for r in self.alive:
                Robot._respond_or_die(r)
            for r in self.alive:
                Robot._execute_drive(r)
            for r1, r2 in combinations(self.alive, 2):
                if Robot._get_distance(r1, r2) < HITBOX:
                    r1._status.damage += 2
                    r2._status.damage += 2
            round += 1
            yield
        winner = self.alive[0]._status.id if len(self.alive) == 1 else None
        return (round, winner)
