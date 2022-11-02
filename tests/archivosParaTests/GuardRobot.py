class GuardRobot(Robot):  # noqa: F821
    def initialize(self):
        self.dir = 90

    def respond(self):
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

        self.point_scanner(0, 10)
        result = self.scanned()

        if result is not None and self.is_cannon_ready():
            self.cannon(0, min(result, 699))
