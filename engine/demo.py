from engine import Game

a = """
class A(Robot):
    def initialize(self):
        pass

    def respond(self):
        pass

"""
b = """
class IDieAt3(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        if self.a == 3: raise Exception("Robot B was baddd")
        self.a += 1
"""
c = """
class IDieAt7(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        if self.a == 7: raise Exception("Robot C was baddd")
        self.a += 1
"""
d = """
class IRun(Robot):
    def initialize(self):
        self.a = 1

    def respond(self):
        self.drive(0,100)
"""


def demo():
    g = Game([("A", a), ("IDieAt3", b), ("IDieAt7", c), ("IRun", d)], 10)
    return g.simulate()
