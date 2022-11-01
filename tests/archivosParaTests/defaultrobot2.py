class GuardRobot(Robot):  # noqa: F821
    def initialize(self):
        self.dir = 90

    def respond(self):
        import random
        x, y = self.get_position()
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

        if self.is_cannon_ready():
            self.cannon(0, random.uniform(100, 800))
