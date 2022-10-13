from .robot import Robot, Position
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
        self.rounds = rounds
        self.robots: List[Robot] = []
        init_data = zip(range(1, 5), robot_descriptions, STARTPOS)
        for num, (name, code), pos in init_data:
            try:
                exec(code)
                robot = eval(name)()
                assert isinstance(robot, Robot)
            except Exception:
                robot = Robot()
                robot._status.damage = 100
            robot._status.position = pos
            robot._status.name = f"{num}-{name}"
            self.robots.append(robot)

    @property
    def alive(self) -> List[Robot]:
        return [r for r in self.robots if r._status.damage < 100]

    def simulate(self):
        result = {"robots": {}}
        for r in self.robots:
            result["robots"][r._status.name] = {"positions": [], "damage": []}
        for r in self.alive:
            try:
                r.initialize()
            except Exception:
                r._status.damage = 100

        for round in range(self.rounds):
            for r in self.robots:
                x = r._status.position.x
                y = r._status.position.y
                damage = r._status.damage
                result["robots"][r._status.name]["positions"].append(
                    {"x": x, "y": y}
                )
                result["robots"][r._status.name]["damage"].append(damage)

            for r in self.alive:
                r.respond()

            if len(self.alive) <= 1:
                break
        return result
