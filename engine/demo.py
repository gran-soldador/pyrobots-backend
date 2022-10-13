from engine import Game

a = """
class A(Robot):
    def initialize(self):
        pass

    def respond(self):
        pass

"""
b = """
class B(Robot):
    def initialize(self):
        pass

    def respond(self):
        pass

"""
g = Game([("A", a), ("B", b)], 10)
g.simulate()
