from robot import Robot, Position
from typing import List, Tuple

MAXX = 1000.0
MAXY = 1000.0
STARTPOS = [
    Position(.1 * MAXX, .1 * MAXY),
    Position(.1 * MAXX, .9 * MAXY),
    Position(.9 * MAXX, .9 * MAXY),
    Position(.9 * MAXX, .1 * MAXY),
]


class Game:
    def __init__(self,
                 robot_descriptions: List[Tuple[str, str]],
                 rounds: int = 100000):
        assert 2 <= len(robot_descriptions) <= 4
        assert 1 <= rounds <= 100000
        self.robots = []
        for (name, code), pos in zip(robot_descriptions, STARTPOS):
            try:
                exec(code)
                robot = eval(name)()
                assert issubclass(robot, Robot)
            except Exception:
                robot = Robot()
                robot._status.damage = 100
            robot._status.position = pos
            robot._status.name = name
            self.robots.append(robot)
