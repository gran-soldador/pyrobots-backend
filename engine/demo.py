from engine import Game

random = (1, "RandomRobot", """
class RandomRobot(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        import random
        self.drive(random.uniform(0,360),50)
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
""")


def demo():
    g = Game([random, square, dvd, spiral])
    return g.simulation()
