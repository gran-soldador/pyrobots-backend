import random

from engine import Game
from engine.constants import MAXROUNDS


def test_invalid_codes():
    # Is not code
    r1 = (1, "A", """
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Maecenas semper arcu in metus dignissim consectetur.
Nam consequat vulputate ullamcorper.
    """)
    # Wrong class name
    r2 = (2, "MyRobot", """
class NotMyRobot(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    # Doesn't subclass Robot
    r3 = (3, "MyObj", """
class MyObj():
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    # Good Robot
    r4 = (4, "MyGoodRobot", """
class MyGoodRobot(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    gut = Game([r1, r2, r3, r4], 100)
    assert len(gut.alive) == 1
    assert gut.alive[0]._status.name == r4[1]


def test_moving_robots():
    r = (1, "R", """
class R(Robot):
    def initialize(self):
        pass
    def respond(self):
        self.drive(45,1)
    """)
    rounds = 5
    gut = Game([r, r], rounds)
    result = gut.simulation()
    assert result.maxrounds == result.rounds_played == rounds
    assert len(result.rounds) == result.rounds_played + 1
    for prev, curr in zip(result.rounds, result.rounds[1:]):
        assert (curr.robots[0].x > prev.robots[0].x and
                curr.robots[0].y > prev.robots[0].y)


def test_sleeping_robots():
    r = (1, "R", """
class R(Robot):
    def initialize(self):
        pass
    def respond(self):
        from time import sleep
        sleep(2)
        self.drive(45,1)
    """)
    rounds = 5
    gut = Game([r, r], rounds)
    result = gut.simulation()
    assert result.maxrounds == result.rounds_played == rounds
    assert len(result.rounds) == result.rounds_played + 1
    for prev, curr in zip(result.rounds, result.rounds[1:]):
        assert (curr.robots[0].x == prev.robots[0].x and
                curr.robots[0].y == prev.robots[0].y)


def test_early_finish():
    r1 = (1, "ISurvive", """
class ISurvive(Robot):
    def initialize(self):
        pass
    def respond(self):
        pass
    """)
    r2 = (2, "IDieAt3", """
class IDieAt3(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        if self.a == 3: raise Exception("Robot B was baddd")
        self.a += 1
""")
    rounds = 100
    gut = Game([r1, r2], rounds)
    result = gut.simulation()
    assert result.rounds_played == 3
    assert result.players[1].name == r2[1]
    assert len(result.rounds) == result.rounds_played + 1
    for status in result.rounds[:-1]:
        assert status.robots[1].damage == 0
    assert result.rounds[-1].robots[1].damage == 100


def test_crashing_robots():
    def r(n):
        return (n, "IGoToCenter", """
class IGoToCenter(Robot):
    def initialize(self):
        pass
    def respond(self):
        x,y=self.get_position()
        if x < 500:
            if y < 500: #lower left
                self.drive(45+0,50)
            else: #upper left
                self.drive(45+270, 50)
        else:
            if y < 500: #lower right
                self.drive(45+90, 50)
            else: #upper right
                self.drive(45+180, 50)
    """)
    gut = Game([r(1), r(2), r(3), r(4)], MAXROUNDS)
    result = gut.simulation()

    assert result.rounds_played < MAXROUNDS
    count = sum(1 for robot in result.rounds[-1].robots
                if robot.damage >= 100)
    assert count >= 3


def test_shooting_robot():
    random.seed(1)

    def r(n):
        return (n, "IGoToCenter", """
class IGoToCenter(Robot):
    def initialize(self):
        pass
    def respond(self):
        x,y=self.get_position()
        if x < 500:
            if y < 500: #lower left
                self.drive(45+0,50)
            else: #upper left
                self.drive(45+270, 50)
        else:
            if y < 500: #lower right
                self.drive(45+90, 50)
            else: #upper right
                self.drive(45+180, 50)
        if self.is_cannon_ready():
            self.cannon(random.uniform(0,360),random.uniform(100,400))
    """)
    shooter = (100, "ShooterRobot", """
class ShooterRobot(Robot):
    def initialize(self):
        self.a = 1
    def respond(self):
        from math import atan2, sqrt, degrees
        x, y = self.get_position()
        x -= 500
        y -= 500
        angle, distance = degrees(atan2(y,x)), sqrt(x**2 + y**2)
        if self.is_cannon_ready():
            self.cannon((angle+180)%360, distance)
""")
    gut = Game([r(1), r(2), r(3), shooter], MAXROUNDS)
    result = gut.simulation()

    assert len(result.rounds[-1].missiles) > 0
    assert sum(len(r.explosions) for r in result.rounds[-10:]) > 0
    assert result.rounds_played < MAXROUNDS
    assert len(result.winners) == 1 and result.winners[0].id == 100


square = (3, "SquareRobot", """
class SquareRobot(Robot):
    def initialize(self):
        self.cycling_mode = False

    def respond(self):
        x, y = self.get_position()
        vel, dir = self.get_velocity(), self.get_direction()
        if not self.cycling_mode:
            if x <= 980: self.drive(0, 50)
            else:
                self.drive(90, 50)
                self.cycling_mode = True
        else:
            preds = [x < 20, x > 980, y < 20, y > 980]
            if sum(1 for pred in preds if pred) == 1: self.drive(dir, 100)
            else: self.drive((dir + 90)%360, 50)
""")

dvd = (4, "DVDRobot", """
class DVDRobot(Robot):
    def initialize(self):
        pass
    def respond(self):
        x, y = self.get_position()
        vel, dir = self.get_velocity(), self.get_direction()
        if vel == 0:
            self.drive(random.uniform(0,360), 25)
        elif x == 1000 or x == 0 or y == 1000 or y == 0:
            self.drive(random.uniform(dir+90, dir+270)%360,25)
        else:
            self.drive(dir, 25)
        if self.is_cannon_ready(): self.cannon(dir, 80)
""")

spiral = (5, "SpiralRobot", """
class SpiralRobot(Robot):
    def initialize(self):
        pass
    def respond(self):
        x, y = self.get_position()
        vel, dir = self.get_velocity(), self.get_direction()
        if vel == 0:
            self.drive(random.uniform(0,360),50)
        else:
            self.drive((dir + 5) % 360, 50)
        if self.is_cannon_ready(): self.cannon(dir, 80)
""")

guard = (15, "GuardRobot", """
class GuardRobot(Robot):
    def initialize(self):
        self.dir = 90

    def respond(self):
        x, y = self.get_position()
        vel, dir = self.get_velocity(), self.get_direction()

        if x < 100:
            self.drive(0, 50)
        elif x > 150:
            self.drive(180, 50)
        else:
            if y > 900:
                self.dir = 270
            elif y < 100:
                self.dir = 90
            self.drive(self.dir, 50)

        self.point_scanner(0, 10)
        result = self.scanned()

        if result is not None and self.is_cannon_ready():
            self.cannon(0, result)
""")

config = ([guard, square, dvd, spiral], 10000)


def demo_game():
    g = Game(*config)
    return g.simulation()


def demo_match():
    g = Game(*config)
    return g.match()


def test_match_equals_simulation():
    random.seed(1)
    match = demo_match()
    random.seed(1)
    sim = demo_game()
    assert match.players == sim.players
    assert match.winners == sim.winners
    assert match.rounds_played == sim.rounds_played
