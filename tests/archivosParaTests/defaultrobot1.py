class defaultrobot1(Robot):
    def initialize(self):
        pass

    def respond(self):
        x, y = self.get_position()
        vel, dir = self.get_velocity(), self.get_direction()
        if vel == 0:
            self.drive(random.uniform(0, 360), 50)
        else:
            self.drive((dir + 5) % 360, 50)
