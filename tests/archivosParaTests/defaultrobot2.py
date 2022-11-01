class defaultrobot2(Robot):
    def initialize(self):
        pass

    def respond(self):
        x, y = self.get_position()
        vel, dir = self.get_velocity(), self.get_direction()
        if vel == 0:
            self.drive(random.uniform(0, 360), 25)
        elif x == 1000 or x == 0 or y == 1000 or y == 0:
            self.drive(random.uniform(dir + 90, dir + 270) % 360, 25)
        else:
            self.drive(dir, 75)
