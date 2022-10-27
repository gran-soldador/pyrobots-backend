class RandomRobot(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        import random
        self.drive(random.uniform(0, 360), 50)
