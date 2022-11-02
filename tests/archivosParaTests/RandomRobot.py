class RandomRobot(Robot):  # noqa: F821

    def initialize(self):
        self.a = 1

    def respond(self):
        from math import atan2, sqrt, degrees
        import random
        dir = (self.get_direction() + random.uniform(-90, 90) + 360) % 360
        x, y = self.get_position()
        x -= 500
        y -= 500
        angle, distance = degrees(atan2(y, x)), sqrt(x**2 + y**2)
        if distance > 400:
            dir = (angle + 360 + 180) % 360
        self.drive(dir, 50)
        if self.is_cannon_ready():
            self.cannon(dir, 150)
