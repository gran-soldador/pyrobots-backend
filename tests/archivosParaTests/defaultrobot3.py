class SpiralRobot(Robot):  # noqa: F821
    def initialize(self):
        pass

    def respond(self):
        import random
        vel, dir = self.get_velocity(), self.get_direction()
        if vel == 0:
            self.drive(random.uniform(0, 360), 50)
        else:
            self.drive((dir + 5) % 360, 50)
        if self.is_cannon_ready():
            self.cannon(dir, 80)
