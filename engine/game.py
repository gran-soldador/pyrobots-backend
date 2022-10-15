from .robot import Robot, Position
from typing import Any, Generator, List, Tuple
import logging

MAXX = 1000.0
MAXY = 1000.0
STARTPOS = [
    (.1 * MAXX, .1 * MAXY),
    (.1 * MAXX, .9 * MAXY),
    (.9 * MAXX, .9 * MAXY),
    (.9 * MAXX, .1 * MAXY),
]


class Game:
    def __init__(self,
                 robot_descriptions: List[Tuple[str, str]],
                 rounds: int = 100000):
        assert 2 <= len(robot_descriptions) <= 4
        assert 1 <= rounds <= 100000
        logging.getLogger(__name__).debug("starting game")
        self.rounds = rounds
        self.robots: List[Robot] = []
        init_data = zip(range(4), robot_descriptions, STARTPOS)
        for num, (name, code), xy in init_data:
            try:
                exec(code)
                robot = eval(name)()
                assert isinstance(robot, Robot)
            except Exception:
                logging.getLogger(__name__).debug(
                    "Robot failed during construction", exc_info=True)
                robot = Robot()
                robot._status.damage = 100
            robot._status.position = Position(*xy)
            robot._status.name = name
            robot._status.id = num
            self.robots.append(robot)

    @property
    def alive(self) -> List[Robot]:
        return [r for r in self.robots if r._status.damage < 100]

    def simulate(self):
        result = {
            "robots": [{
                "name": r._status.name,
                "positions": [],
                "damage": []
            } for r in self.robots]
        }

        self._initialize_robots()

        round_generator = self._execute_rounds()
        finished = False
        while True:
            for r in self.robots:
                x = r._status.position.x
                y = r._status.position.y
                damage = r._status.damage
                result["robots"][r._status.id]["positions"].append(
                    {"x": x, "y": y}
                )
                result["robots"][r._status.id]["damage"].append(damage)
            if finished:
                break
            try:
                next(round_generator)
            except StopIteration as ret:
                result["rounds"], result["winner"] = ret.args[0]
                if result["rounds"] != self.rounds:
                    # Early finish! Must do one last iteration to write data
                    finished = True
                else:
                    break
        return result

    def _initialize_robots(self):
        for r in self.alive:
            self._robot_do_or_die(r.initialize)

    def _execute_rounds(self) -> Generator[Any, None, Tuple[int, int]]:
        round = 1
        while round <= self.rounds:
            for r in self.alive:
                self._robot_do_or_die(r.respond)
            if len(self.alive) <= 1:
                break
            round += 1
            yield
        winner = self.alive[0]._status.id if len(self.alive) == 1 else None
        return (round, winner)

    def _robot_do_or_die(self, method):
        try:
            method()
        except Exception:
            logging.getLogger(__name__).debug("Robot failed when called",
                                              exc_info=True)
            method.__self__._status.damage = 100
