from engine import Game

random = (1, "RandomRobot", """
class RandomRobot(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        from math import atan2, sqrt, degrees
        dir = (self.get_direction() + random.uniform(-90,90) + 360) % 360
        x, y = self.get_position()
        x -= 500
        y -= 500
        angle, distance = degrees(atan2(y,x)), sqrt(x**2 + y**2)
        if distance > 400:
            dir = (angle +360+180) % 360
        self.drive(dir, 50)
        if self.is_cannon_ready():
            self.cannon(dir, 150)
""")

sleeping = (2, "SleepingRobot", """
class SleepingRobot(Robot):
    def initialize(self):
        pass

    def respond(self):
        pass
""")

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


def demo():
    g = Game(*config)
    return g.simulation()


def demo_match():
    g = Game(*config)
    return g.match()
